"""Process ownership guard: stopping our launch must leave unrelated processes alive."""
import importlib.util,json,os,signal,subprocess,sys,time
from pathlib import Path


def test_stop_reaps_orphan_descendant_and_preserves_unrelated_process(tmp_path,monkeypatch):
    script=Path(__file__).resolve().parents[2]/'tools/robot_processes.py'
    spec=importlib.util.spec_from_file_location('robot_processes',script)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    marker='robot-tools-test-'+str(os.getpid())
    unrelated=subprocess.Popen([sys.executable,'-c','import time;time.sleep(40)'])
    child_file=tmp_path/'child'
    code="import subprocess,sys; p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(40)']);open(sys.argv[1],'w').write(str(p.pid))"
    parent=subprocess.Popen([sys.executable,'-c',code,str(child_file)],env=dict(os.environ,TEAM_STACK_RUN_ID=marker))
    parent.wait(timeout=3)
    module.state=tmp_path/'launch.json';module.state.write_text(json.dumps({'run_id':marker}))
    # Use the real process signalling, but don't clean the machine's DDS resources in a unit test.
    original_run=module.subprocess.run
    monkeypatch.setattr(module.subprocess,'run',lambda *args,**kwargs:subprocess.CompletedProcess(args,0,'',''))
    try:
        assert module.owned(marker)
        module.stop()
        assert not module.owned(marker)
        assert unrelated.poll() is None
        assert not module.state.exists()
    finally:
        unrelated.terminate();unrelated.wait(timeout=3)
        for pid,_ in module.owned(marker):os.kill(pid,signal.SIGKILL)


def test_camera_override_preserves_other_service_arguments(tmp_path):
    script=Path(__file__).resolve().parents[2]/'tools/robot_camera.py'
    spec=importlib.util.spec_from_file_location('robot_camera',script)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    text='ROS_DOMAIN_ID=7\nEXTRA_LAUNCH_ARGS="foo:=bar camera_config:=rgbstereo camera_params:=/old"\n'
    result=module.camera_override(text,Path('/new.yaml'))
    assert 'ROS_DOMAIN_ID=7' in result and 'foo:=bar' in result
    assert 'camera_config:=rgbd' in result and 'camera_params:=/new.yaml' in result
    assert '/old' not in result
    assert module.camera_override(result,Path('/new.yaml'))==result



def test_competition_camera_driver_configuration_preserves_clock_and_alignment():
    import yaml
    directory=Path(__file__).resolve().parents[1]/'config'
    mapping=yaml.safe_load((directory/'oak_hardware.yaml').read_text())['/oak']['ros__parameters']
    mission=yaml.safe_load((directory/'oak_competition.yaml').read_text())['/oak']['ros__parameters']
    assert mission['camera']==mapping['camera']
    for stream in ('rgb','stereo'):
        assert [mission[stream][key] for key in ('i_width','i_height','i_fps')]==[640,360,5.]
        assert mission[stream]['i_get_base_device_timestamp'] is False
        assert mission[stream]['i_update_ros_base_time_on_ros_msg'] is True
        assert mission[stream]['i_max_q_size']==1
        assert [mapping[stream][key] for key in ('i_width','i_height')]==[1280,720]
    assert mission['stereo']['i_align_depth'] is True
    assert mission['rgb']['i_isp_num']/mission['rgb']['i_isp_den']==1/3

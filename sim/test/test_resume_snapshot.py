import json,os,subprocess,time
from pathlib import Path
import rclpy
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
from rclpy.qos import qos_profile_sensor_data
from std_srvs.srv import Empty


def test_resume_snapshot_requests_stationary_amcl_update_and_preserves_map(tmp_path,monkeypatch):
    # Isolated ROS test; no hardware or simulator.
    monkeypatch.setenv('ROS_DOMAIN_ID','151');monkeypatch.setenv('ROS_AUTOMATIC_DISCOVERY_RANGE','LOCALHOST')
    rclpy.init();node=rclpy.create_node('resume_snapshot_fixture')
    pose=node.create_publisher(PoseWithCovarianceStamped,'/slam/pose',10)
    odom=node.create_publisher(Odometry,'/odom',qos_profile_sensor_data)
    calls=[]
    def update(request,response):
        calls.append(True);m=PoseWithCovarianceStamped();m.header.frame_id='map'
        m.header.stamp=node.get_clock().now().to_msg();m.pose.pose.position.x=2.
        m.pose.covariance[0]=.02;pose.publish(m);return response
    node.create_service(Empty,'/request_nomotion_update',update)
    def wheel():
        m=Odometry();m.header.stamp=node.get_clock().now().to_msg();odom.publish(m)
    node.create_timer(.05,wheel)
    (tmp_path/'map.yaml').write_text('{}')
    data=dict(format_version=1,map_yaml='map.yaml',landmarks={str(i):{} for i in range(8)},final_pose=[0.,0.,0.],final_pose_covariance=[0.]*36)
    source=tmp_path/'snapshot.json';source.write_text(json.dumps(data));output=tmp_path/'resume.json'
    tool=Path(__file__).parents[2]/'tools/robot_resume_snapshot.py'
    child=subprocess.Popen(['/usr/bin/python3',str(tool),'--source',str(source),'--output',str(output),'--timeout','5'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    try:
        end=time.monotonic()+8
        while child.poll() is None and time.monotonic()<end:rclpy.spin_once(node,timeout_sec=.02)
        if child.poll() is None:child.kill()
        log=child.communicate(timeout=3)[0];assert child.returncode==0,log
        result=json.loads(output.read_text());assert calls
        assert result['final_pose']==[2.,0.,0.] and result['final_pose_covariance'][0]==.02
        assert Path(result['map_yaml'])==tmp_path/'map.yaml'
        assert json.loads(source.read_text())==data
    finally:
        if child.poll() is None:child.kill();child.wait()
        node.destroy_node();rclpy.shutdown()

import importlib.util
from pathlib import Path


def test_top_cpu_uses_interval_frame_not_boot_average():
    script=Path(__file__).resolve().parents[2]/'tools/robot_load.py'
    spec=importlib.util.spec_from_file_location('robot_load',script)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    output='top - first\n PID USER %CPU COMMAND\n 12 robot 80.0 python\ntop - second\n PID USER %CPU COMMAND\n 12 robot 4.2 python\n'
    assert module.parse_top(output)=={12:4.2}

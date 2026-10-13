# Team Autonomy Stack

This repository contains the ROS 2 software written by our team for an autonomous
mobile-robot project. It combines mapping and localization, mission planning,
camera/lidar perception, Nav2 control, docking, collision-safe escape behavior,
shared ROS interfaces, and a multi-robot evaluation harness.

The export is intentionally source-only. It contains no robot-vendor source,
mission-server source, credentials, trained models, maps, ROS bags, experiment
recordings, build products, or internal team logs.

## Packages

| Package | Purpose |
|---|---|
| `team_interfaces` | Shared messages for missions, docks, predictions, health, trajectories, and coordination |
| `team_slam` | `slam_toolbox`/AMCL integration, dock-tag mapping, snapshots, and wheel/IMU odometry |
| `team_planning` | Mission adapter, dock occupancy, autonomous exploration, and camera coverage |
| `team_control` | Nav2 coordinator, docking adapter, collision-safe escape, and hardware command handling |
| `team_control_docking` | Open Navigation docking plugin for tag-relative non-charging docks |
| `team_control_mppi_critic` | Prediction-aware MPPI critic plugin |
| `team_perception` | Detector adapters, multi-cue ranging, tracking, prediction, and dock-state inference |
| `team_sim` | Multi-robot simulation and evaluation code; requires an external robot simulation package |

## Supported environment

- Ubuntu 24.04
- ROS 2 Jazzy
- Nav2 Jazzy
- Gazebo Harmonic
- Python 3.12

The core packages use standard ROS 2 and Nav2 interfaces. `team_sim` and the
hardware launch profile are integration adapters: users must provide their own
robot description, Gazebo bringup, sensor drivers, mission service, and model
files. Those dependencies are deliberately not included here.

## Build

```bash
mkdir -p ~/team_ws/src
cd ~/team_ws/src
git clone YOUR_GITHUB_URL team-autonomy-stack
cd team-autonomy-stack
./tools/fetch_dependencies.sh

cd ~/team_ws
source /opt/ros/jazzy/setup.bash
export PYTHONNOUSERSITE=1
rosdep install --from-paths \
  src/team-autonomy-stack/src/team_interfaces \
  src/team-autonomy-stack/src/team_slam \
  src/team-autonomy-stack/src/team_planning \
  src/team-autonomy-stack/src/team_control \
  src/team-autonomy-stack/src/team_control_docking \
  src/team-autonomy-stack/src/team_control_mppi_critic \
  src/team-autonomy-stack/src/team_perception \
  src/team-autonomy-stack/vendor_src/m-explore-ros2/explore \
  src/team-autonomy-stack/vendor_src/m-explore-ros2/explore_lite_msgs \
  --ignore-src -r -y
colcon build --symlink-install \
  --base-paths src/team-autonomy-stack/src src/team-autonomy-stack/vendor_src \
  --packages-up-to team_interfaces team_slam team_planning team_control \
    team_control_docking team_control_mppi_critic team_perception explore_lite
```

`team_sim` is skipped in the public core build because its robot model and
bringup packages are external. Build it after supplying equivalent integration
packages and adapting its launch and model references to your platform.

## Tests

```bash
source /opt/ros/jazzy/setup.bash
export PYTHONNOUSERSITE=1
source ~/team_ws/install/setup.bash
colcon test --packages-select team_interfaces team_slam team_planning team_control \
  team_control_docking team_control_mppi_critic team_perception
colcon test-result --verbose
```

`PYTHONNOUSERSITE=1` prevents unrelated packages installed under `~/.local`
from overriding the Python libraries supplied with ROS 2 and Ubuntu.

## Integration boundary

The autonomy packages consume standard ROS lidar, RGB/depth image, camera-info,
joint-state, IMU, odometry, occupancy-grid, TF, and Nav2 interfaces. The optional
`team_sim` adapter requires a separately supplied robot description and simulator
bringup. Its package manifest, world launch, model resolver, and truth entity names
must be adapted to a different robot.

The mission service remains behind a small HTTP adapter. Supply a compatible
external service with `--mission-source` or `TEAM_MISSION_SOURCE`, or replace the
adapter with manual goals. Hardware parameters are examples and must be measured
on the target platform. The collision monitor must remain the final publisher to
the physical velocity command topic.

## Configuration and credentials

All physical values are ROS parameters with units and comments in `config/`.
Credentials are accepted only through runtime environment variables. Do not put
tokens, passwords, model files, maps, snapshots, or recordings in this repository.
See [SECURITY.md](SECURITY.md) before publishing or deploying.

## License

Team-authored source in this export is licensed under Apache License 2.0. External
dependencies retain their own licenses and are fetched separately.

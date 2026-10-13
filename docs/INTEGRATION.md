# Integration boundary

The autonomy packages expect standard ROS interfaces:

- `sensor_msgs/LaserScan` for lidar;
- `sensor_msgs/Image` and `CameraInfo` for RGB/depth;
- `sensor_msgs/JointState` and IMU angular velocity for the optional odometry node;
- `nav_msgs/Odometry`, `OccupancyGrid`, and REP-105 transforms;
- Nav2 planner, controller, behavior, collision-monitor, docking, AMCL, and map-server APIs.

The exported `team_sim` package was written around an external robot model and
bringup package. Those packages are not part of this repository. To use the
simulator publicly, adapt these files to your robot:

- `src/team_sim/package.xml` — replace the external robot package dependencies;
- `src/team_sim/launch/world.launch.py` — launch your simulator bringup;
- `src/team_sim/team_sim/world.py` — resolve your model and initial world entities;
- `src/team_sim/team_sim/truth_node.py` — map simulator entity names to evaluation IDs.

The mission client is isolated behind a small HTTP adapter. Replace it with your
own mission source or use manual goals. No server implementation or credentials
are included. The experiment runner accepts the external checkout through
`--mission-source` (or `TEAM_MISSION_SOURCE`) and never assumes a private sibling
repository.

Hardware launch parameters are examples derived from one platform and remain
provisional until measured on a new robot. The collision monitor must remain the
final publisher to the physical velocity command topic.

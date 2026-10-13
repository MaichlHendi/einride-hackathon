# Third-party and external components

This repository contains only team-authored source plus small patches authored by
the team. It does not redistribute:

- the robot vendor's application, bringup, description, hardware, or simulation repositories;
- the mission server implementation or its data;
- `m-explore-ros2` source;
- trained detector models or TensorRT/ONNX runtimes;
- maps, recordings, logs, credentials, or generated evaluation artifacts.

`m-explore-ros2` is fetched from its upstream repository at a pinned revision and
keeps its upstream license. The patches under `dependencies/patches/` contain only
our changes.

Names of external ROS packages and topics remain in integration adapters where
needed to describe the dependency boundary. They do not include external source.

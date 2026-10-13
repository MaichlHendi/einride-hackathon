# team_control_docking

C++ Open Navigation docking plugin for tag-relative, non-charging docks. The
`team_control::TagDock` plugin selects live tag observations and applies lateral,
heading, and dock-axis acceptance limits before reporting success.

The plugin declaration is in `docks.xml`; its implementation is
`src/tag_dock.cpp`.

```bash
colcon build --packages-select team_control_docking
colcon test --packages-select team_control_docking
```

# team_control_mppi_critic

C++ critic plugin for Nav2 MPPI. `mppi::critics::PredictionCritic` adds a soft,
probability-weighted cost when candidate motion approaches predicted robot
trajectories, including probability mass outside explicit modes.

The plugin declaration is in `critics.xml`; parameters are configured through
`team_control/config/control.yaml`.

```bash
colcon build --packages-select team_control_mppi_critic
colcon test --packages-select team_control_mppi_critic
```

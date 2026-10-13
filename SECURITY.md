# Security and publication policy

Never commit robot or mission-service credentials, `.env` files, private network
addresses, model weights, calibration captures, maps, snapshots, ROS bags, logs,
or generated experiment data.

Secrets are runtime inputs. The mission token uses `TEAM_SAGA_TOKEN`; simulation
tokens and administrator credentials are generated per run. Keep ROS parameter
event recording disabled when secrets are passed as parameters.

Before pushing a release, run:

```bash
./tools/publication_audit.sh
git status --short
git ls-files | sort
```

The audit is conservative and does not replace review by the code owners. Report
a suspected exposed credential privately to the maintainers; do not open a public
issue containing the value.

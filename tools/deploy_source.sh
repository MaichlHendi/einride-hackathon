#!/usr/bin/env bash
set -euo pipefail

if [[ $# != 1 || ! $1 =~ ^[A-Za-z0-9_.-]+@[A-Za-z0-9_.-]+$ ]]; then
  echo 'Usage: tools/deploy_source.sh user@host' >&2
  exit 2
fi

target=$1
project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
remote_workspace=${TEAM_REMOTE_WORKSPACE:-team_ws}

command -v rsync >/dev/null
command -v ssh >/dev/null

ssh "$target" "mkdir -p \"\$HOME/$remote_workspace/src/team-autonomy-stack\""
rsync -az --delete \
  --exclude='.git/' --exclude='build/' --exclude='install/' --exclude='log/' \
  --exclude='data/' --exclude='results/' --exclude='bags/' --exclude='maps/' \
  --exclude='vendor_src/' --exclude='*.db3' --exclude='*.mcap' --exclude='*.bag' \
  --exclude='*.engine' --exclude='*.onnx' --exclude='.env*' --exclude='*.token' \
  "$project_root/" "$target:$remote_workspace/src/team-autonomy-stack/"

cat <<EOF
Source copied to $target:~/$remote_workspace/src/team-autonomy-stack
On the target, source its ROS underlay and run:
  cd ~/$remote_workspace/src/team-autonomy-stack
  ./tools/fetch_dependencies.sh
  cd ~/$remote_workspace
  export PYTHONNOUSERSITE=1
  colcon build --symlink-install --base-paths src/team-autonomy-stack/src src/team-autonomy-stack/vendor_src \\
    --packages-up-to team_interfaces team_slam team_planning team_control \\
      team_control_docking team_control_mppi_critic team_perception explore_lite
EOF

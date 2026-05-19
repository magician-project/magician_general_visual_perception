#!/bin/bash
# Container entrypoint: source ROS, build custom messages, activate venv.
set -e

source /opt/ros/rolling/setup.bash

ROS_WS="/home/${USER}/ros_ws"
WORKSPACE="/home/${USER}/workspace"

# Build the magician_vision_classifier ROS package (msgs/srvs) if not already built.
# Must happen here because the package lives in the volume-mounted workspace.
if [ ! -f "${ROS_WS}/install/setup.bash" ]; then
    echo "[entrypoint] Building ROS workspace..."
    mkdir -p "${ROS_WS}/src"
    ln -sfn "${WORKSPACE}" "${ROS_WS}/src/magician_vision_classifier"
    cd "${ROS_WS}"
    colcon build --symlink-install
    echo "[entrypoint] Build complete."
fi

source "${ROS_WS}/install/setup.bash"

source "/home/${USER}/venv/bin/activate"

# Launch the Y-MAP-Net ROS node in the background if the model exists.
# The node is registered as ros2 run magician_general_visual_perception ymapnet_node.py
MODEL_DIR="${WORKSPACE}/Y-MAP-Net/2d_pose_estimation"
if [ -d "$MODEL_DIR" ]; then
    echo "[entrypoint] Starting ymapnet_node..."
    ros2 run magician_general_visual_perception ymapnet_node.py \
        --ros-args -p input_topic:=/camera/image_raw \
        >> /tmp/ymapnet_node.log 2>&1 &
    echo "[entrypoint] ymapnet_node started (PID $!). Log: /tmp/ymapnet_node.log"
else
    echo "[entrypoint] Model not found at ${MODEL_DIR}."
    echo "[entrypoint] Run: cd \${WORKSPACE}/Y-MAP-Net && bash scripts/downloadModel.sh"
    echo "[entrypoint] Then restart the container to activate the node."
fi

exec "$@"

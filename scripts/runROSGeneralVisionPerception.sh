#!/bin/bash

# Resolve paths from this script so it works from any working directory.
# readlink -f follows symlinks, so a link to this script outside the repo works too.
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")" || exit 1
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
PACKAGE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)" || exit 1
WORKSPACE_DIR="$(cd "$PACKAGE_DIR/../.." && pwd)" || exit 1
YMAP_DIR="$PACKAGE_DIR/Y-MAP-Net"

if [[ ! -f "$WORKSPACE_DIR/install/setup.bash" ]]; then
    echo "ROS workspace setup not found: $WORKSPACE_DIR/install/setup.bash" >&2
#    exit 1
fi
if [[ ! -x "$YMAP_DIR/runYMAPNet.sh" ]]; then
    echo "Y-MAP-Net launcher not found: $YMAP_DIR/runYMAPNet.sh" >&2
    exit 1
fi

# runYMAPNet.sh selects venv or venv_jax itself. Check the default venv here
# so a missing environment cannot silently fall back to the system Python.
use_default_venv=1
previous_arg=
for arg in "$@"; do
    if [[ "$arg" == --collab || ( "$previous_arg" == --engine && "$arg" == jax ) ]]; then
        use_default_venv=0
    fi
    previous_arg="$arg"
done
if (( use_default_venv )) && [[ ! -f "$YMAP_DIR/venv/bin/activate" || ! -x "$YMAP_DIR/venv/bin/python3" ]]; then
    echo "Y-MAP-Net venv not found: $YMAP_DIR/venv (run $PACKAGE_DIR/scripts/setup.sh)" >&2
    exit 1
fi

# Load ROS first; the Y-MAP-Net launcher then activates the selected venv.
source "$WORKSPACE_DIR/install/setup.bash" || exit 1

# This host has glibc 2.35, while the locally built TensorFlow wheel needs
# 2.38. Use a matching loader and libraries for this Python process only.
GLIBC_LIB_DIR="$PACKAGE_DIR/.runtime/glibc-2.39/usr/lib/x86_64-linux-gnu"
glibc_version="$(getconf GNU_LIBC_VERSION 2>/dev/null)"
if [[ "$glibc_version" =~ ^glibc[[:space:]]+([0-9]+)\.([0-9]+)$ ]] &&
   (( use_default_venv && (BASH_REMATCH[1] < 2 || (BASH_REMATCH[1] == 2 && BASH_REMATCH[2] < 38)) )); then
    if [[ ! -x "$GLIBC_LIB_DIR/ld-linux-x86-64.so.2" ]]; then
        echo "Local glibc runtime is missing. Run $PACKAGE_DIR/scripts/setup_local_glibc_runtime.py" >&2
        exit 1
    fi
    export YMAPNET_GLIBC_LIB_DIR="$GLIBC_LIB_DIR"
fi

cd "$YMAP_DIR" || exit 1
exec ./runYMAPNet.sh --from /dev/video4 "$@"

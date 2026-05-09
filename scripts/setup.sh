#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/.."

YMAP_NET_DIR="Y-MAP-Net"
YMAP_NET_REPO="https://github.com/FORTH-ICS-CVRL-HCCV/Y-MAP-Net.git"

if [ ! -d "$YMAP_NET_DIR" ]; then
    echo "Cloning Y-MAP-Net..."
    git clone "$YMAP_NET_REPO" "$YMAP_NET_DIR"
fi

exec "$YMAP_NET_DIR/scripts/setup.sh" "$@"

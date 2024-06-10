#!/bin/sh
set -eu
mkdir -p /data/db/.config/rclone
cp /conf/rclone.conf /data/db/.config/rclone/rclone.conf

exec "$@"
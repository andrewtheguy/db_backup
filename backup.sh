#!/bin/bash
set -euo pipefail
rclone mkdir sftp:mongobackup
mongodump --uri="$MONGO_URI" --archive=/tmp/backup
rclone copyto /tmp/backup "sftp:/mongobackup/$BACKUP_DIR/$(date +%Y-%m-%d_%H-%M-%S).dump"
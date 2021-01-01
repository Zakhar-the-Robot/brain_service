#!/bin/bash
set -e # exit when any command fails
SCRIPT_ROOT=$(dirname $(readlink -f "$0"))
SCRIPT_NAME=$(basename "$0")
function log { echo "- $1 [$(basename "$0")]" ;}
# ----------------------------------------------------------------------------

SERVICE_FILE_NAME="zakhar_display.service"

log "Stopping the service: $SERVICE_FILE_NAME"
systemctl stop $SERVICE_FILE_NAME

log "Starting the service: $SERVICE_FILE_NAME"
systemctl start $SERVICE_FILE_NAME

log "[ Done ]"


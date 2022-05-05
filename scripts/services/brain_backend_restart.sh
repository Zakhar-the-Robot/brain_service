#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi
set -e # exit when any command fails
SCRIPT_ROOT=$(dirname $(readlink -f "$0"))
SCRIPT_NAME=$(basename "$0")
function log { echo "- $1 [$(basename "$0")]" ;}
# ----------------------------------------------------------------------------

SERVICE_FILE_NAME="brain_backend.service"

log "Stopping the service: $SERVICE_FILE_NAME"
systemctl stop $SERVICE_FILE_NAME

log "Reload: $SERVICE_FILE_NAME"
systemctl daemon-reload

log "Starting the service: $SERVICE_FILE_NAME"
systemctl start $SERVICE_FILE_NAME

log "[ Done ]"


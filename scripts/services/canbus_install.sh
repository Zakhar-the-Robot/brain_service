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

SERVICE_FILE_NAME="canbus.service"
SERVICE_SRC_FILE_PATH="$SCRIPT_ROOT/$SERVICE_FILE_NAME"
SERVICE_DSC_FILE_PATH="/lib/systemd/system/$SERVICE_FILE_NAME"


if [ ! -f $SERVICE_DSC_FILE_PATH ]; then
    log "Creating a $SERVICE_FILE_NAME file"
else
    log "$SERVICE_FILE_NAME exists! The service will be updated"
    log "Stopping the service: $SERVICE_FILE_NAME"
    systemctl stop $SERVICE_FILE_NAME
    rm $SERVICE_DSC_FILE_PATH
fi

log "Writing the service"
cp "$SERVICE_SRC_FILE_PATH" "$SERVICE_DSC_FILE_PATH"

log "Reloading systemctl daemons"
systemctl daemon-reload

log "Enabling the service"
systemctl enable $SERVICE_FILE_NAME

log "Starting the service: $SERVICE_FILE_NAME"
systemctl start $SERVICE_FILE_NAME

log "[ Done ]"


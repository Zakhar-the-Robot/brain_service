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

SERVICE_FILE_NAME="zakhar.service"
SERVICE_FILE_PATH="/lib/systemd/system/$SERVICE_FILE_NAME"


if [ ! -f $SERVICE_FILE_PATH ]; then
    log "$SERVICE_FILE_NAME does not exist."
else
    log "Disabling the service"
    systemctl disable $SERVICE_FILE_NAME
    log "Stopping the service: $SERVICE_FILE_NAME"
    systemctl stop $SERVICE_FILE_NAME
    rm $SERVICE_FILE_PATH
    log "Uninstall canbus.service"
    $SCRIPT_ROOT/services/canbus_uninstall.sh
    log "The service was uninstalled."
fi

log "[ Done ]"


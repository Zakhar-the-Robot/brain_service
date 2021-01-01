#!/bin/bash
set -e # exit when any command fails
SCRIPT_ROOT=$(dirname $(readlink -f "$0"))
SCRIPT_NAME=$(basename "$0")
function log { echo "- $1 [$(basename "$0")]" ;}
# ----------------------------------------------------------------------------

SERVICE_FILE_NAME="zakhar_display.service"
SERVICE_FILE_PATH="/lib/systemd/system/$SERVICE_FILE_NAME"
SERVICE_FILE_CONTENT="[Unit]
Description=Zakhar Display service
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 $SCRIPT_ROOT/display_service.py
StandardInput=tty-force

[Install]
WantedBy=multi-user.target"


if [ ! -f $SERVICE_FILE_PATH ]; then
    log "Creating a $SERVICE_FILE_NAME file"
else
    log "$SERVICE_FILE_NAME exists! The service will be updated"
    log "Stopping the service: $SERVICE_FILE_NAME"
    systemctl stop $SERVICE_FILE_NAME
    rm $SERVICE_FILE_PATH
fi


log "Writing the service"
touch $SERVICE_FILE_PATH
echo "$SERVICE_FILE_CONTENT" > $SERVICE_FILE_PATH

log "Downloading python packages"
/usr/bin/python3 -m pip install --user -r $SCRIPT_ROOT/../requirements.txt

log "Reloading systemctl daemons"
systemctl daemon-reload

log "Enabling the service"
systemctl enable $SERVICE_FILE_NAME

log "Starting the service: $SERVICE_FILE_NAME"
systemctl start $SERVICE_FILE_NAME

log "[ Done ]"


#!/bin/bash
# *************************************************************************
#
# Copyright (c) 2022 Andrei Gramakov. All rights reserved.
#
# This file is licensed under the terms of the MIT license.  
# For a copy, see: https://opensource.org/licenses/MIT
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi
set -e # exit when any command fails
SCRIPT_ROOT=$(dirname $(readlink -f "$0"))
SCRIPT_NAME=$(basename "$0")
function log { echo "- $1 [$(basename "$0")]" ;}
# ----------------------------------------------------------------------------

SERVICE_FILE_NAME="brain.service"
SERVICE_FILE_PATH="/lib/systemd/system/$SERVICE_FILE_NAME"


if [ ! -f $SERVICE_FILE_PATH ]; then
    log "$SERVICE_FILE_NAME does not exist."
else
    log "Disabling the service"
    systemctl disable $SERVICE_FILE_NAME
    log "Stopping the service: $SERVICE_FILE_NAME"
    systemctl stop $SERVICE_FILE_NAME
    rm $SERVICE_FILE_PATH
    log "The service was uninstalled."
fi

log "[ Done ]"


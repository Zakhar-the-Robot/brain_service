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

log "Status brain_frontend.service"
systemctl status brain_frontend.service

log "Status brain_backend.service"
systemctl status brain_backend.service

log "Status canbus.service"
systemctl status canbus.service


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

log "Uninstall brain_backend.service"
$SCRIPT_ROOT/services/brain_backend_uninstall.sh

log "Uninstall brain_service_display.service"
$SCRIPT_ROOT/services/brain_service_display_uninstall.sh

log "Uninstall canbus.service"
$SCRIPT_ROOT/services/canbus_uninstall.sh

log "[ Done ]"


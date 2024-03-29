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

log "Installation of the Zakhar Brain Service..."
echo ""

bash $SCRIPT_ROOT/python/packages_download.sh
bash $SCRIPT_ROOT/python/packages_install_symlinks.sh

bash $SCRIPT_ROOT/services/canbus_install.sh
bash $SCRIPT_ROOT/services/brain_service_install.sh
bash $SCRIPT_ROOT/services/brain_service_display_install.sh

echo ""
log "[ Done ]"


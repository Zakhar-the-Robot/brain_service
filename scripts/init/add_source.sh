#!/bin/bash
# *************************************************************************
#
# Copyright (c) 2021 Andrei Gramakov. All rights reserved.
#
# This file is licensed under the terms of the MIT license.  
# For a copy, see: https://opensource.org/licenses/MIT
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************

set -e # exit when any command fails
SCRIPT_ROOT=$(dirname $(readlink -f "$0"))
SCRIPT_NAME=$(basename "$0")
function log { echo "- $1 [$(basename "$0")]" ;}

# *************************************************************************

PROFILE=/etc/profile.d/zakhar.sh

LINE=". /zakhar/scripts/zakhar_profile.sh"

if [ ! -f $PROFILE ]; then
    log "Creating a $PROFILE file"
    touch $PROFILE
fi

log "Write to the $PROFILE file"
echo "$LINE" > $PROFILE

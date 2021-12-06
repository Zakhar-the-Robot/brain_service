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

source $SCRIPT_ROOT/dirs.sh

ZAKHAR_UGROUP="ZakharUsers"

log "Create directories"
mkdir -p $DIR_SHARED
mkdir -p $DIR_PY
mkdir -p $DIR_SRV
mkdir -p $DIR_SCR
mkdir -p $DIR_ROS

log "Create a group ${ZAKHAR_UGROUP} and direcrtories config"

if [ $(getent group $ZAKHAR_UGROUP) ]; then
    log "Group is already exists"
else
    groupadd $ZAKHAR_UGROUP
fi
chgrp -R $ZAKHAR_UGROUP $DIR_SHARED
chmod -R 777 $DIR_SHARED
chown -R root:${ZAKHAR_UGROUP} $DIR_SHARED

log "Add users to ${ZAKHAR_UGROUP}"
usermod -a -G $ZAKHAR_UGROUP root
usermod -a -G $ZAKHAR_UGROUP mind


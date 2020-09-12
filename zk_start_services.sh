#!/bin/bash
SCRIPT_ROOT=$(dirname $(readlink -f "$0"))
SCRIPT_NAME=$(basename "$0")
function log { echo "- $1 [$(basename "$0")]" ;}
# ----------------------------------------------------------------------------


IS_DISPLAY_STARTED=$(pgrep -f '/usr/local/bin/python3 -m display' 2>&1)
log $IS_DISPLAY_STARTED
if [ -z $IS_DISPLAY_STARTED ] ; then
    log "Display start"
    PYTHONPATH="$SCRIPT_ROOT:$PYTHONPATH"
    /usr/local/bin/python3 -m display 2>&1 &
fi


IS_ROS_STARTED=$(pgrep roscore 2>&1)
log $IS_ROS_STARTED
if [ -z $IS_ROS_STARTED ] ; then
    log "Starting roscore"
    roscore 2>&1 &
fi
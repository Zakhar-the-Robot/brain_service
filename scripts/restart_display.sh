#!/bin/bash
SCRIPT_ROOT=$(dirname $(readlink -f "$0"))
SCRIPT_NAME=$(basename "$0")
function log { echo "- $1 [$(basename "$0")]" ;}
# ----------------------------------------------------------------------------

source "$SCRIPT_ROOT/vars.sh"
kill $(pgrep -f '/usr/local/bin/python3 -m display') 2>&1
PYTHONPATH="$ZKSERVICE_PATH:$PYTHONPATH"
/usr/local/bin/python3 -m display >> $HOME/zakhar_display.log &

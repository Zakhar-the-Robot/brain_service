SCRIPT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME=$(basename ${BASH_SOURCE[0]})
function log { echo "- $1 [$SCRIPT_NAME]" ;}
# ----------------------------------------------------------------------------
# shellcheck disable=SC2128,SC2169,SC2039 # ignore array expansion warning
if [ -n "${BASH_SOURCE}" ] && [ "${BASH_SOURCE[0]}" = "${0}" ]
then
    echo "This script should be sourced, not executed:"
    # shellcheck disable=SC2039  # reachable only with bash
    echo ". ${SCRIPT_ROOT}/${SCRIPT_NAME}"
    exit 1
fi
# ----------------------------------------------------------------------------
source "$SCRIPT_ROOT/scripts/vars.sh"

echo -e "******* Zakhar *******\n"
echo -e "\$ZKBRAIN_PATH: $ZKBRAIN_PATH"
echo -e "\$ZKCORE_PATH: $ZKCORE_PATH"
echo -e "\$ZKPY_PATH: $ZKPY_PATH"
echo -e "\$ZKSERVICE_PATH: $ZKSERVICE_PATH"
echo -e "\n**********************\n"

export PATH="$HOME/.poetry/bin:$PATH"  # TODO delete

export PATH="$ZKSERVICE_PATH:$ZKCORE_PATH:$PATH"
export PYTHONPATH="$ZKBRAIN_PATH:$ZKPY_PATH:$PYTHONPATH"
export PYTHONPATH="$ZKCORE_PATH/devel/lib/python3/dist-packages:$PYTHONPATH"


source /opt/ros/noetic/setup.bash
if [ -f "$ZKCORE_PATH/devel/setup.sh" ]; then
    source "$ZKCORE_PATH/devel/setup.sh"
fi

bash "$ZKSERVICE_PATH/zk_start_services.sh"

# if $ret -ne 0
# then
#     echo "Display start"
#     # PYTHONPATH="/home/mind/zakhar_service:$PYTHONPATH"
#     # /usr/local/bin/python3 -m display >> $HOME/zakhar_display.log &
# fi
SCRIPT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME=$(basename ${BASH_SOURCE[0]})
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
export ZKBRAIN_PATH=$(dirname "$(dirname $SCRIPT_ROOT)")
export ZKSERVICE_PATH="$ZKBRAIN_PATH/zakhar_service"
export ZKCORE_PATH="$ZKBRAIN_PATH/zakharos_core"
export ZKPY_PATH="$ZKBRAIN_PATH/zakharos_pycore"

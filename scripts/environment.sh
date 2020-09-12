#!/bin/bash

# you should source only this file to get everything works
# ----------------------------------------------------------------------------

function abspath {
    if [[ -d "$1" ]]
    then
        pushd "$1" >/dev/null
        pwd
        popd >/dev/null
    elif [[ -e $1 ]]
    then
        pushd "$(dirname "$1")" >/dev/null
        echo "$(pwd)/$(basename "$1")"
        popd >/dev/null
    else
        echo "  $1" does not exist! >&2
        return 127
    fi
}

function read_pythonpath_dirs
{
    SCRIPT_ROOT=$(dirname $(readlink -f "$BASH_SOURCE"))
    pushd $SCRIPT_ROOT >/dev/null
    new_pythonpath=""

    while IFS= read -r line
    do
        abs_path=$(abspath $line)
        if [[ $abs_path ]]
        then
            new_pythonpath="$abs_path:$new_pythonpath"
        fi
    done < "$SCRIPT_ROOT/PYTHONPATH_extra_dirs.txt"

    echo ${new_pythonpath::-1}  #return a value without the last ':'
    popd >/dev/null
}



# ----------------------------------------------------------------------------
# public variables
ZAKHAROS_WS_DIR=$(dirname "$(dirname $(readlink -f "$BASH_SOURCE"))")


if [ -f "/opt/ros/melodic/setup.bash" ]; then
    source /opt/ros/melodic/setup.bash
fi

# PYTHONPATH="$(read_pythonpath_dirs):$PYTHONPATH"

if [ -f "$ZAKHAROS_WS_DIR/devel/setup.bash" ]; then
    source $ZAKHAROS_WS_DIR/devel/setup.bash
fi



#clean functions
unset -f abspath
unset -f read_pythonpath_dirs
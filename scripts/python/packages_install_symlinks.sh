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

set -e # exit when any command fails
SCRIPT_ROOT=$(dirname $(readlink -f "$0"))
SCRIPT_NAME=$(basename "$0")
function log { echo "- $1 [$(basename "$0")]" ;}

# *************************************************************************

log "Install service python packages"

log "Install python package: brain_service_common..."
rm -f "/zakhar/python_packages/brain_service_common"
ln -sf "$SCRIPT_ROOT/../../src/brain_service_common"      "/zakhar/python_packages/brain_service_common"

log "Install python package: brain_service_backend..."
rm -f "/zakhar/python_packages/brain_service_backend"
ln -sf "$SCRIPT_ROOT/../../src/brain_service_backend"     "/zakhar/python_packages/brain_service_backend"

log "Install python package: brain_service_display..."
rm -f "/zakhar/python_packages/brain_service_display"
ln -sf "$SCRIPT_ROOT/../../src/brain_service_display"    "/zakhar/python_packages/brain_service_display"

log "Install python package: brain_service..."
rm -f "/zakhar/python_packages/brain_service"
ln -sf "$SCRIPT_ROOT/../../src/brain_service"             "/zakhar/python_packages/brain_service"

log "[ Done ]"

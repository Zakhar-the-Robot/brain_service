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

echo ""
echo "********************"
echo "  Zakhar the Robot"
echo "********************"
echo ""

ZAKHAR=1

ZAKHAR_PYTHONPATH="/zakhar/python_packages"
ZAKHAR_SERVICE="/zakhar/service"
ZAKHAR_ROS_PACKAGE_PATH="/zakhar/ros_packages"

PYTHONPATH="$PYTHONPATH:$ZAKHAR_PYTHONPATH"
ROS_PACKAGE_PATH="$ROS_PACKAGE_PATH:$ZAKHAR_ROS_PACKAGE_PATH"

zakhar_service_status_all() {
    sudo systemctl status canbus.service
    sudo systemctl status brain.service
    sudo systemctl status brain_service_display.service
}

zakhar_service_start(){
    sudo systemctl start brain.service
}
zakhar_service_stop(){
    sudo systemctl stop brain.service
}
zakhar_service_status(){
    sudo systemctl status brain.service
}

zakhar_service_display_start(){
    sudo systemctl start brain_service_display.service
}
zakhar_service_display_stop(){
    sudo systemctl stop brain_service_display.service
}
zakhar_service_display_status(){
    sudo systemctl status brain_service_display.service
}

zakhar_service_canbus_start(){
    sudo systemctl start canbus.service
}
zakhar_service_canbus_stop(){
    sudo systemctl stop canbus.service
}
zakhar_service_canbus_status(){
    sudo systemctl status canbus.service
}

export -f zakhar_service_status_all

export -f zakhar_service_start
export -f zakhar_service_stop
export -f zakhar_service_status

export -f zakhar_service_display_start
export -f zakhar_service_display_stop
export -f zakhar_service_display_status

export -f zakhar_service_canbus_start
export -f zakhar_service_canbus_stop
export -f zakhar_service_canbus_status

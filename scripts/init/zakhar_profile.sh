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
    sudo systemctl status brain_frontend.service
    sudo systemctl status brain_backend.service
    sudo systemctl status canbus.service
}

zakhar_service_start_backend(){
    sudo systemctl start brain_backend.service
}
zakhar_service_stop_backend(){
    sudo systemctl stop brain_backend.service
}
zakhar_service_status_backend(){
    sudo systemctl status brain_backend.service
}

zakhar_service_start_frontend(){
    sudo systemctl start brain_frontend.service
}
zakhar_service_stop_frontend(){
    sudo systemctl stop brain_frontend.service
}
zakhar_service_status_frontend(){
    sudo systemctl status brain_frontend.service
}

zakhar_service_start_canbus(){
    sudo systemctl start canbus.service
}
zakhar_service_stop_canbus(){
    sudo systemctl stop canbus.service
}
zakhar_service_status_canbus(){
    sudo systemctl status canbus.service
}

export -f zakhar_service_status_all

export -f zakhar_service_start_backend
export -f zakhar_service_stop_backend

export -f zakhar_service_start_frontend
export -f zakhar_service_stop_frontend

export -f zakhar_service_start_canbus
export -f zakhar_service_stop_canbus

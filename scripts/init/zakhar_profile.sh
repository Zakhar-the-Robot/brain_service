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

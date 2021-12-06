#!/usr/bin/env python3
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
import os
import subprocess
import psutil
import ifcfg

if psutil.LINUX:
    import pwd

from service_common.internal import is_zakhar_environment
from .common_types import Status
from .decorators import zakhar_only_bool


class Is:
    @staticmethod
    def service_active(name: str) -> bool:
        if os.system('systemctl is-active --quiet %s' % name):
            return False
        else:
            return True

    @staticmethod
    def process_exists(name: str) -> bool:
        result = False
        if psutil.WINDOWS:
            return result
        try:
            subprocess.check_output(f"pidof '{name}'", shell=True)
            result = True
        except subprocess.CalledProcessError:
            pass
        return result

    @classmethod
    def ros(cls) -> bool:
        return cls.process_exists("roscore")

    @classmethod
    def ssh(cls) -> bool:
        return cls.process_exists("sshd")

    @staticmethod
    def zakhar():
        return is_zakhar_environment()

    # TODO Implement a check that the device is in the CAN network
    @staticmethod
    @zakhar_only_bool
    def can_device(device_id=None):
        if not Is.can_driver_installed():
            return Status.UNKNOWN
        return Status.INACTIVE

    @staticmethod
    @zakhar_only_bool
    def can_driver_installed():
        can0 = ifcfg.interfaces().get("can0")
        if can0:
            return "UP" in can0["flags"]
        else:
            return False
    
    @staticmethod
    @zakhar_only_bool 
    def user():
        try:
            pwd.getpwnam('mind')
        except KeyError:
            return False
        return True

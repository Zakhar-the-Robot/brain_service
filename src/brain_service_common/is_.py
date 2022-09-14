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
from datetime import datetime
if psutil.LINUX:
    import pwd

from brain_pycore.logging import log

from brain_service_common.internal import is_zakhar_environment
from brain_service_common.constants import DEFAULT_CAN_PERIOD_SEC
from .common_types import Status
from .decorators import zakhar_only_bool

# TODO:make all methods properties


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

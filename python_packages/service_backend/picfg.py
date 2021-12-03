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
from .files import Files, PATH_RPI_CMDLINE, PATH_RPI_CONFIG, PATH_ZK_CMDLINE, PATH_ZK_CONFIG


class PiCfg():
    @staticmethod
    def set_cmdline_txt() -> bool:
        if not Files.compare(PATH_ZK_CMDLINE, PATH_RPI_CMDLINE):
            Files.write_file_to_file(PATH_ZK_CMDLINE, PATH_RPI_CMDLINE)
            return True
        return False

    @staticmethod
    def set_config_txt() -> bool:
        if not Files.compare(PATH_ZK_CONFIG, PATH_RPI_CONFIG):
            Files.write_file_to_file(PATH_ZK_CONFIG, PATH_RPI_CONFIG)
            return True
        return False

    @staticmethod
    def can_up(bitrate=125000):
        return os.system(f"sudo ip link set can0 up type can bitrate {bitrate}")

    @staticmethod
    def can_down():
        return os.system("sudo ip link set can0 down")

    @staticmethod
    def set_hostname():
        pass

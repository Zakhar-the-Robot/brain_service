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
import socket
from datetime import datetime
import subprocess

from brain_service_common.decorators import zakhar_only_str


class Get:
    @staticmethod
    def host_name():
        return socket.gethostname()

    @staticmethod
    def current_time():
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def host_ip() -> str:
        """This method returns the "primary" IP on the local box (the one with a default route)"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    @staticmethod
    @zakhar_only_str
    def wifi() -> str:
        # TODO Find more reliable solution of getting WIFI name
        try:
            out = subprocess.check_output("iwgetid").decode()
            wf = out.strip("wlan0").strip().strip("ESSID:").strip("\"")
            if str(wf) == "None":
                wf = "Unknown"
        except subprocess.CalledProcessError:
            wf = "[Error]"
        return wf

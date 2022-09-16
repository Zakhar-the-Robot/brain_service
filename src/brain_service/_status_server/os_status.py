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
from .get import Get
from .is_ import Is
from .constants import STATUS_UNKNOWN
from .__status import StatusClass


class OsStatus(StatusClass):
    def __init__(self) -> None:
        self.host = ""
        self.ip = ""
        self.wifi_net = ""
        self.is_mind_user = False
        self.can_up = STATUS_UNKNOWN
        self.ssh_up = STATUS_UNKNOWN
        self.ros_up = STATUS_UNKNOWN
        self.time = None

    def update(self) -> None:
        self.host = Get.host_name()
        self.ip = Get.host_ip()
        self.can_up = Is.can_driver_installed()
        self.ssh_up = Is.ssh()
        self.ros_up = Is.ros()
        self.time = Get.current_time()
        self.is_mind_user = Is.user()
        self.wifi_net = Get.wifi()

if __name__ == "__main__":
    l = OsStatus()
    l.update()
    print(l)
    pass

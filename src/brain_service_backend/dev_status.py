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
from brain_service_common.is_ import Is
from ._status import StatusClass


class DevStatus(StatusClass):
    def __init__(self):
        self.face = -1
        self.sensors = -1
        self.motors = -1
        self.tool = -1

    def update(self):
        self.motors = Is.can_device(0x2) 
        self.face = Is.can_device(0x3) 
        self.sensors = Is.can_device(0x4)
        self.tool = Is.can_device(0x7)

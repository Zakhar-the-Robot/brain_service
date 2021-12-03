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
from service_common.is_ import Is
from ._status import StatusClass


class DevStatus(StatusClass):
    def __init__(self):
        self.face = -1
        self.sensors = -1
        self.motors = -1

    def update(self):
        self.face = Is.can_device("0x2a")
        self.sensors = Is.can_device("0x2b")
        self.motors = Is.can_device("0x2c")

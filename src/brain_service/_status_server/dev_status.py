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
from datetime import datetime
from typing import Dict
from .constants import DEFAULT_CAN_PERIOD_SEC, STATUS_ACTIVE, STATUS_INACTIVE
from .__status import StatusClass

class DevStatus(StatusClass):
    def __init__(self):
        self.face = -1
        self.sensors = -1
        self.motors = -1
        self.tool = -1

    @staticmethod
    def is_device_connected(device_id: int, device_log: Dict[int, datetime]):
        last_dev_upd = device_log.get(device_id)
        if last_dev_upd and (datetime.now().timestamp() - last_dev_upd.timestamp()
                             < DEFAULT_CAN_PERIOD_SEC):
            return STATUS_ACTIVE
        return STATUS_INACTIVE

    def update(self, device_log: Dict[int, datetime]):

        self.motors = self.is_device_connected(0x2, device_log)
        self.face = self.is_device_connected(0x3, device_log)
        self.sensors = self.is_device_connected(0x4, device_log)
        self.tool = self.is_device_connected(0x7, device_log)

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
from brain_pycore.logging import new_logger, LOG_LEVEL

from ._can_server import CanServer
from ._config_monitor import ConfigMonitor
from ._status_server import DevStatus, OsStatus, StatusServer

CANBUS_IN_PORT = 5556    # TODO move to common?
CANBUS_OUT_PORT = 5566    # TODO move to common?
CANBUS_SERVICE_MSG_RCV_TOPIC = "can_rcv"    # TODO move to common?

STATUS_SERVICE_PORT = 5557    # TODO move to common?
STATUS_SERVICE_TOPIC = "status"    # TODO move to common?


class ZakharService:
    def __init__(self,
                 no_connection=False,
                 config_monitor=False,
                 log_level=LOG_LEVEL.INFO) -> None:
        self.log = new_logger("Back", log_level=log_level)
        self.no_connection = no_connection
        self.config_monitor = config_monitor

        self.can_server = CanServer(out_msg_port=CANBUS_OUT_PORT,
                                    in_msg_port=CANBUS_IN_PORT,
                                    in_msg_topic=CANBUS_SERVICE_MSG_RCV_TOPIC,
                                    log_level=log_level)
        self.status_server = StatusServer(port=STATUS_SERVICE_PORT,
                                          topic=STATUS_SERVICE_TOPIC,
                                          can_dev_log=self.can_server.device_log,
                                          log_level=log_level)
        self.config_monitor = ConfigMonitor(self.status_server.status)
        

    def __del__(self):
        self.stop()

    def __repr__(self) -> str:
        return str(self.status)

    def start(self):
        self.can_server.start()
        self.status_server.start()
        if self.config_monitor:
            self.config_monitor.start()

    def stop(self):
        self.can_server.stop()
        self.status_server.stop()
        self.config_monitor.stop()

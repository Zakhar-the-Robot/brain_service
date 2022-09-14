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
from logging import INFO
from time import sleep
import errno

from brain_pycore.thread import StoppableThread
from brain_pycore.logging import new_logger, LOG_LEVEL

from brain_service_backend.dev_status import DevStatus
from brain_service_backend.picfg import PiCfg
from brain_service_common.is_ import Is
from brain_service_common.constants import DEFAULT_BACKEND_PORT, DEFAULT_BACKEND_HOST
from .os_status import OsStatus
from ._can_server import CanServer
from ._status_server import StatusServer
import socket


class ZakharServiceBackend:
    def __init__(self,
                 no_connection=False,
                 config_monitor=False,
                 log_level=LOG_LEVEL.INFO) -> None:
        self.log = new_logger("Back", log_level=log_level)
        self.no_connection = no_connection
        self.config_monitor = config_monitor
        self.status = {"os": OsStatus(), "dev": DevStatus(),
                       "service": {}, "err": {}, "warn": {}}

        self.thread_cfg_monitor = None  # type: StoppableThread | None

        self.can_server = CanServer()
        self.status_server = StatusServer(self.can_server.device_log)

    def __del__(self):
        self.stop()

    def __repr__(self) -> str:
        return str(self.status)

    def _configure(self):
        # TODO add /etc/profile configuration
        if not Is.can_driver_installed():
            error = PiCfg.can_up()
            if error:
                self.log.error(f"Error: {error}")
        if PiCfg.set_cmdline_txt():
            self.status["service"]["cmdline_upd"] = True
        if PiCfg.set_config_txt():
            self.status["service"]["config_upd"] = True

    def cfg_monitor_target(self):
        while True:
            sleep(5)
            self._configure()

    def start(self):
        self.can_server.start()
        self.status_server.start()
        if self.config_monitor:
            self.thread_cfg_monitor = StoppableThread(target=self.cfg_monitor_target)
            self.thread_cfg_monitor.start()

    def stop(self):
        self.can_server.stop()
        self.status_server.stop()
        if self.thread_cfg_monitor:
            self.thread_cfg_monitor.stop()
            self.thread_cfg_monitor = None

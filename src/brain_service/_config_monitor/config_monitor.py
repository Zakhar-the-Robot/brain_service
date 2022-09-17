# *************************************************************************
#
# Copyright (c) 2022 Andrei Gramakov. All rights reserved.
#
# This file is licensed under the terms of the MIT license.  
# For a copy, see: https://opensource.org/licenses/MIT
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************

from time import sleep
from brain_pycore.thread import StoppableThread
import ifcfg
from .picfg import PiCfg


class ConfigMonitor:

    def __init__(self, status: dict):
        self.status = status
        self.thread_cfg_monitor = None  # type: StoppableThread | None

    def start(self):
        self.thread_cfg_monitor = StoppableThread(target=self.cfg_monitor_target)
        self.thread_cfg_monitor.start()

    @staticmethod
    def can_driver_installed():
        can0 = ifcfg.interfaces().get("can0")
        if can0:
            return "UP" in can0["flags"]
        else:
            return False

    def _configure(self):
        # TODO add /etc/profile configuration
        if not self.can_driver_installed():
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

    def stop(self):
        if self.thread_cfg_monitor:
            self.thread_cfg_monitor.stop()
            self.thread_cfg_monitor = None

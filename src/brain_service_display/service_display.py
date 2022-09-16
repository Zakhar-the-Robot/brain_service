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

from psutil import WINDOWS as IS_WINDOWS
from typing import Union
import ast

from brain_pycore.thread import StoppableThread
from brain_pycore.logging import new_logger, LOG_LEVEL
from brain_pycore.zmq import ZmqPublisherThread, ZmqSubscriberThread
from brain_service_common.common_types import Status

from .display import Display


class ServiceDisplay:
    ERROR_SYMBOL = "e"
    WARNING_SYMBOL = "w"
    STATUS_SERVICE_PORT = 5557
    STATUS_SERVICE_TOPIC = "status"

    def __init__(self, log_level=LOG_LEVEL.INFO) -> None:
        self.log = new_logger("Front", log_level=log_level)
        self.thread_display = None  # type: Union[StoppableThread, None]
        self.thread_reader = None  # type: Union[ZmqPublisherThread, None]
        self.display = Display(IS_WINDOWS)
        self.data = {}

    def __del__(self):
        self.stop()

    def _display_network(self):
        os = self.data.get("os")
        if os:
            self.display.show_mm(f"IP: {os.get('ip')}",
                                 f"Net: {os.get('wifi_net')}", 1)

    def _display_os_status(self):
        ssh, can, ros = " ", " ", " "
        if self.data.get("os"):
            if self.data["os"]["ssh_up"]:
                ssh = "x"
            if self.data["os"]["can_up"]:
                can = "x"
            if self.data["os"]["ros_up"]:
                ros = "x"
        self.display.show_mm(f"SSH: [{ssh}] | CAN: [{can}]",
                             f"ROS: [{ros}]", 
                             1)

    def _display_devices(self):
        def _get_dev_str(devs) -> str:
            d_str = ""
            if devs and devs.keys():
                for dev, val in devs.items():
                    if val == Status.ACTIVE:
                        val = "x"
                    elif val == Status.INACTIVE:
                        val = " "
                    elif val == Status.NA:
                        val = "/"
                    else:
                        val = "?"
                    d_str += f"[{val}]{dev[0]} "
            return d_str.strip()

        dev = self.data.get("dev")
        if dev:
            self.display.show_mm(f"Devices:",
                                 _get_dev_str(self.data["dev"]), 2)

    def _display_intro(self):
        self.display.show_l("Hello!", 1)
        self.display.show_l("I am Zakhar!", 1)

    def _display_all_once(self):
        self._display_network()
        self._display_os_status()
        self._display_devices()

    def display_all(self):
        self._display_intro()
        while True:
            self._display_all_once()

    def _callback_sub(self, msg):
        # TODO: use json instead?
        new_data = ast.literal_eval(msg)  # convert input string to python code
        self.data = new_data
        self.log.debug(f"{self.data}")

    def start(self):
        self.thread_reader = ZmqSubscriberThread(self.STATUS_SERVICE_PORT,
                                                 self.STATUS_SERVICE_TOPIC,
                                                 callback=self._callback_sub)
        self.thread_display = StoppableThread(target=self.display_all)
        self.thread_display.start()
        self.thread_reader.start()

    def stop(self):
        self.log.info("Terminating...")
        if self.display:
            self.display.show_l("Turn off", 1)
        if self.thread_display:
            self.thread_display.stop()

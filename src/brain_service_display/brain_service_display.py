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


class BrainServiceDisplay:
    ERROR_SYMBOL = "e"
    WARNING_SYMBOL = "w"
    STATUS_SERVICE_PORT = 5557
    STATUS_SERVICE_TOPIC = "status"

    def __init__(self, log_level=LOG_LEVEL.INFO) -> None:
        self.log = new_logger("Front", log_level=log_level)
        self.thread_display = None  # type: Union[StoppableThread, None]
        self.thread_reader = None  # type: Union[ZmqPublisherThread, None]
        self.display = Display(IS_WINDOWS)
        self.markers = {"err": "", "warn": ""}
        self.data = {}

    def __del__(self):
        self.stop()

    def _get_markers_str(self) -> str:
        s = ""
        for m in self.markers.values():
            s += m
        if s:
            s = s + " | "
        return s

    def _display_errors_and_warns(self):
        if self.data.get("err") and self.data["err"].keys():
            self.markers["err"] = self.ERROR_SYMBOL
            for err, msg in self.data["err"].items():
                self.display.show_mm(f"{self.ERROR_SYMBOL} | Error: {err}", msg, 2)
        else:
            self.markers["err"] = ""

        if self.data.get("warn") and self.data["warn"].keys():
            self.markers["warn"] = self.WARNING_SYMBOL
            for wrn, msg in self.data["warn"].items():
                self.display.show_mm(f"{self.WARNING_SYMBOL} | Warn: {wrn}", msg, 1)
        else:
            self.markers["warn"] = ""

    def _display_os_status(self):
        os = self.data.get("os")
        if os:
            # self.display.show_sl(f"{self._get_markers_str()} Time:", os.get("time"), .5)
            self.display.show_mm(f"{self._get_markers_str()}IP: {os.get('ip')}",
                                 f"Net: {os.get('wifi_net')}", 1)

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
            self.display.show_mm(f"{self._get_markers_str()}Devices:",
                                 _get_dev_str(self.data["dev"]), 2)

    def _display_intro(self):
        self.display.show_l("Hello!", 1)
        self.display.show_l("I am Zakhar!", 1)

    def _display_all_once(self):
        self._display_errors_and_warns()
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

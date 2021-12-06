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
import time
from psutil import WINDOWS as IS_WINDOWS
from service_common import StoppableThread, log
from service_common.common_types import Status
from .display import Display
import socket
import ast


class ZakharServiceFrontend:
    ERROR_SYMBOL = "e"
    WARNING_SYMBOL = "w"

    def __init__(self, log_level=log.INFO) -> None:
        self.log = log.get_logger("Front", log_level=log_level)
        self.thread_main = None  # type: StoppableThread | None
        self.thread_reader = None  # type: StoppableThread | None
        self.display = Display(IS_WINDOWS)
        self.markers = {"err": "", "warn": ""}
        self.data = {}
        self.socket = None
        self.start()

    def __del__(self):
        self.stop()

    def _connect(self):
        self.log.info("Connecting ...")

        HOST = '127.0.0.1'  # The server's hostname or IP address
        PORT = 65500  # The port used by the server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        self.log.info("Connect!")

    def _receive_backend_data(self):
        if self.socket:
            self.log.debug(f"Receiving...")
            new_data_raw = self.socket.recv(1024).decode()
            new_data = ast.literal_eval(new_data_raw)
            self.data = new_data
            self.log.debug(f"{self.data}")

    def _reader_main(self):
        while True:
            try:
                self._connect()
                break
            except ConnectionRefusedError:
                t = 2
                self.log.warn(f"Connection refused! Wait for {t} sec and retry...")
                time.sleep(t)
        while True:
            self._receive_backend_data()

    def _get_markers_str(self) -> str:
        s = ""
        for m in self.markers.values():
            s += m
        if s:
            s = s + " | "
        return s


    def _show_errors_and_warns(self):
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

    def _show_os_status(self):
        os = self.data.get("os")
        if os:
            # self.display.show_sl(f"{self._get_markers_str()} Time:", os.get("time"), .5)
            self.display.show_mm(f"{self._get_markers_str()}IP: {os.get('ip')}",
                                 f"Net: {os.get('wifi_net')}", 1)


    def _show_devices(self):
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
                    d_str += f"{dev[0]}:[{val}] "
            return d_str.strip()

        dev = self.data.get("dev")
        if dev:
            self.display.show_mm(f"{self._get_markers_str()}Devices:",
                                 _get_dev_str(self.data["dev"]), 1)


    def _main_intro(self):
        self.display.show_l("Hello!", 1)
        self.display.show_l("I am Zakhar!", 1)

    def _main_once(self):
        self._show_errors_and_warns()
        self._show_os_status()
        self._show_devices()

    def main(self):
        self._main_intro()
        while True:
            self._main_once()

    def start(self):
        self.thread_reader = StoppableThread(target=self._reader_main)
        self.thread_main = StoppableThread(target=self.main)
        self.thread_main.start()
        self.thread_reader.start()

    def stop(self):
        if self.display:
            self.display.show_l("Turn off", 1)
        self.thread_main.stop()

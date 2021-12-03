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
from time import sleep
from service_backend.dev_status import DevStatus
from service_backend.picfg import PiCfg
from service_backend.files import Files, PATH_ZK_CONFIG, PATH_RPI_CMDLINE, PATH_RPI_CONFIG, PATH_ZK_CMDLINE
from service_common import StoppableThread, log
from service_common.is_ import Is
from .os_status import OsStatus
import socket


class ZakharServiceBackend:
    def __init__(self, update_period_ms=250, no_connection=False, config_monitor=False, log_level=log.INFO) -> None:
        self.log = log.get_logger("Back", log_level=log_level)
        self.no_connection = no_connection
        self.config_monitor = config_monitor
        self.update_period_ms = 0
        self.status = {"os": OsStatus(), "dev": DevStatus(), "service": {}, "err": {}, "warn": {}}
        self.thread_main = None  # type: StoppableThread | None
        self.thread_cfg_monitor = None  # type: StoppableThread | None
        self.start(update_period_ms)
        self.connection_conn = None  # type: socket.socket | None
        self.connection_addr = None

    def __del__(self):
        self.stop()

    def __repr__(self) -> str:
        return str(self.status)

    def _wait_for_connection(self):
        HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
        PORT = 65500  # Port to listen on (non-privileged ports are > 1023)
        self.log.info("Server: Wait for connection ...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            self.connection_conn, self.connection_addr = s.accept()
            self.log.info("Server: Connect!")

    def _get_full_status_dict(self):
        d = {}
        # Convert all to dict
        for k, v in self.status.items():
            v_dict = None
            if isinstance(v, dict):
                v_dict = v
            elif isinstance(v, object):
                v_dict = vars(v)
            else:
                try:
                    v_dict = dict(v)
                except TypeError:
                    self.log.error("Cannot convert to dict")
            if v_dict:
                d[k] = v_dict
        return d

    def _send_data(self):
        if self.connection_conn:
            to_send = self._get_full_status_dict()
            self.log.debug(f"Server: to send: {str(to_send)}")
            self.connection_conn.sendall(str(to_send).encode())

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

    # TODO move error indication to frontend
    def _update_errors_and_warns(self):
        self.status["err"] = {}
        self.status["warn"] = {}
        if not Is.ros():
            self.status["warn"]["ros"] = "ROS is down"
        if not Is.ssh():
            self.status["err"]["ssh"] = "SSH is down"
        if not Is.can_driver_installed():
            self.status["warn"]["can"] = "CAN is down"

    def _main_once(self):
        self._update_errors_and_warns()
        self.status['os'].update()
        self.status['dev'].update()
        self.log.debug(f"Server status: {self._get_full_status_dict()}")
        self._send_data()
        sleep(self.update_period_ms / 1000)

    def _start_init(self):
        if not self.no_connection:
            self._wait_for_connection()

    def cfg_monitor(self):
        while True:
            sleep(5)
            self._configure()

    def main(self):
        self._start_init()
        while True:
            self._main_once()

    def start(self, update_period_ms=250):
        self.update_period_ms = update_period_ms
        self.thread_main = StoppableThread(target=self.main)
        self.thread_main.start()
        if self.config_monitor:
            self.thread_cfg_monitor = StoppableThread(target=self.cfg_monitor)
            self.thread_cfg_monitor.start()

    def stop(self):
        if self.thread_main:
            self.thread_main.stop()

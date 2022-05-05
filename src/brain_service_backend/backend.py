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
from brain_pycore.logging import new_logger
from brain_pycore.can import canbus

from brain_service_backend.dev_status import DevStatus
from brain_service_backend.picfg import PiCfg
from brain_service_common.is_ import Is
from brain_service_common.constants import DEFAULT_BACKEND_PORT, DEFAULT_BACKEND_HOST
from .os_status import OsStatus
import socket


class ZakharServiceBackend:
    def __init__(self, update_period_ms=250, no_connection=False, config_monitor=False, log_level=INFO) -> None:
        self.log = new_logger("Back", log_level=log_level)
        self.no_connection = no_connection
        self.config_monitor = config_monitor
        self.update_period_ms = 0
        self.status = {"os": OsStatus(), "dev": DevStatus(), "service": {}, "err": {}, "warn": {}}
        
        self.thread_main = None  # type: StoppableThread | None
        self.thread_cfg_monitor = None  # type: StoppableThread | None
        self.thread_connection = None  # type: StoppableThread | None
        self.thread_can_listener = None  # type: StoppableThread | None
        
        self.connection_conn = None  # type: socket.socket | None
        self.connection_addr = None
        canbus.start()
        self.start(update_period_ms)

    def __del__(self):
        self.stop()

    def __repr__(self) -> str:
        return str(self.status)

    def _wait_for_connection(self):
        self.log.info("Server: Wait for connection ...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # make it reusable
            s.bind((DEFAULT_BACKEND_HOST, DEFAULT_BACKEND_PORT))
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
            try:
                self.connection_conn.sendall(str(to_send).encode())
            except IOError as e:
                if e.errno == errno.EPIPE:
                    pass

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
            self.thread_connection = StoppableThread(target=self._wait_for_connection)
            self.thread_connection.start()

    def cfg_monitor_target(self):
        while True:
            sleep(5)
            self._configure()

    def main_target(self):
        self._start_init()
        while True:
            self._main_once()

    def start(self, update_period_ms=250):
        self.update_period_ms = update_period_ms
        self.thread_main = StoppableThread(target=self.main_target)
        self.thread_main.start()
        if self.config_monitor:
            self.thread_cfg_monitor = StoppableThread(target=self.cfg_monitor_target)
            self.thread_cfg_monitor.start()

    def stop(self):
        if getattr(self, "thread_main", None):
            self.thread_main.stop()

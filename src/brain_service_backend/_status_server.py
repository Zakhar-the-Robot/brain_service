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
from datetime import datetime
from typing import Dict, List, Union
from brain_pycore.zmq import (ZmqPublisherThread, ZmqSubscriberThread, ZmqServerThread, ZmqClientThread)
from brain_pycore.logging import new_logger, LOG_LEVEL
from brain_service_backend.dev_status import DevStatus
from brain_service_backend.os_status import OsStatus
from brain_service_common.is_ import Is


class StatusServer:
    STATUS_SERVICE_PORT = 5557
    STATUS_SERVICE_TOPIC = "status"

    def __init__(self, can_dev_log=None):
        self._can_device_log = can_dev_log
        self._log = new_logger(name="StatusServer")
        self._thread = None  # type: Union[ZmqPublisherThread, None]

        self.status = {"os": OsStatus(), 
                       "dev": DevStatus(), 
                       "service": {}, 
                       "err": {}, 
                       "warn": {}}

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
                    self._log.error("Cannot convert to dict")
            if v_dict:
                d[k] = v_dict
        return d

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

    def _callback(self):
        self._update_errors_and_warns()
        self.status['os'].update()
        if self._can_device_log:
            self.status['dev'].update(self._can_device_log)
        to_send = self._get_full_status_dict()
        self._log.debug(f"Server status: {to_send}")
        return to_send
        

    def start(self):
        if self._thread and self._thread.is_alive:
            self._log.warning("Already started")
        else:
            self._thread = ZmqPublisherThread(port=self.STATUS_SERVICE_PORT,
                                              topic=self.STATUS_SERVICE_TOPIC,
                                              publish_callback=self._callback,
                                              thread_name="StatusServer thread",
                                              publishing_freq_hz=2)
            self._thread.start(log_level=LOG_LEVEL.INFO)

    def stop(self):
        self._thread.stop()
        self._thread = None

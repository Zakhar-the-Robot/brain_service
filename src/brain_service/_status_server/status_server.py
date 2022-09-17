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

from typing import Union
from brain_pycore.zmq import ZmqPublisherThread
from brain_pycore.logging import new_logger, LOG_LEVEL
from .dev_status import DevStatus
from .os_status import OsStatus


class StatusServer:

    def __init__(self, port: int, topic: str,
                 can_dev_log=None, log_level=LOG_LEVEL.INFO):
        self._port = port
        self._topic = topic
        self._can_device_log = can_dev_log
        self._log = new_logger(name="StatusServer", log_level=log_level)
        self._thread = None  # type: Union[ZmqPublisherThread, None]

        self.status = {"os": OsStatus(),
                       "dev": DevStatus(),
                       "service": {}}

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

    def _callback(self):
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
            self._thread = ZmqPublisherThread(port=self._port,
                                              topic=self._topic,
                                              publish_callback=self._callback,
                                              thread_name="StatusServer thread",
                                              publishing_freq_hz=2)
            self._thread.start(log_level=LOG_LEVEL.WARNING)

    def stop(self):
        self._thread.stop()
        self._thread = None

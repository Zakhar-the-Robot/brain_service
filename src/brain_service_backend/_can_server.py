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

import ast
from datetime import datetime
from typing import Dict, List, Union
from brain_pycore.zmq import ZmqPublisherThread, ZmqServerThread
from brain_pycore.logging import new_logger, LOG_LEVEL
import can


class CanServer:
    CANBUS_IN_PORT = 5556    # TODO move to common?
    CANBUS_OUT_PORT = 5566    # TODO move to common?
    CANBUS_SERVICE_MSG_RCV_TOPIC = "can_rcv"    # TODO move to common?

    def __init__(self):
        self._log = new_logger(name="CanServer")
        self._thread_in_msg_publisher = None  # type: Union[ZmqPublisherThread, None]
        self._thread_out_msg_server = None  # type: Union[ZmqServerThread, None]
        self._started = False
        self._dev_can = None
        self.device_log = {}  # type: Dict[int,datetime]

    def _callback_publisher(self):
        self._log.debug("_callback_publisher")
        msg = self._dev_can.recv()  # type: Union[can.Message, None]
        self._log.debug(f"msg: 0x{msg.arbitration_id:x} - {msg.data.hex()}")
        if msg:
            id = (msg.arbitration_id >> 8) & 0xF
            now = datetime.now()
            if id:
                self.device_log[id] = now
        msg_str = "{" + f"'id': '0x{msg.arbitration_id:x}', 'data': '{msg.data.hex()}'" + "}"
        return msg_str

    def _callback_out_server(self, request):
        try:
            msg = ast.literal_eval(request)
        except Exception as e:
            return str(e)
        if not isinstance(msg, dict):
            return "Wrong msg format!"

        id = msg["id"]
        data = msg["data"]

        # ID validation
        if id < 0 or id > 2047:
            return f"ID value is out of 11-bit range ({id})"

        # Data validation
        if not isinstance(data, list):
            return f"Wrong data type! Data type is {type(data)}"
        if len(data) > 8:
            return f"Wring request: too many data bytes (data: {data})"
        for d in data:
            if d < 0 or d > 255 or not isinstance(d, int):
                return f"Data value is out of uint8 range ({d})"

        try:
            self.send(id, data)
            result = "ok"
        except Exception as e:
            result = str(e)
        return result

    @property
    def is_stopped(self):
        return not self._started

    @property
    def is_started(self):
        return self._started

    def start(self):
        self._dev_can = can.interface.Bus(channel='can0', bustype='socketcan')
        if self.is_stopped:
            self._thread_in_msg_publisher = ZmqPublisherThread(port=self.CANBUS_IN_PORT,
                                                               topic=self.CANBUS_SERVICE_MSG_RCV_TOPIC,
                                                               publish_callback=self._callback_publisher,
                                                               thread_name="CanServer_in",
                                                               publishing_freq_hz=0)
            self._thread_in_msg_publisher.start(log_level=LOG_LEVEL.WARNING)
            self._thread_out_msg_server = ZmqServerThread(port=self.CANBUS_OUT_PORT,
                                                          callback=self._callback_out_server,
                                                          thread_name="CanServer_out")
            self._thread_out_msg_server.start(log_level=LOG_LEVEL.INFO)
            self._started = True
        else:
            self._log.warning("Already started")

    def stop(self):
        if self.is_started:
            if self._thread_in_msg_publisher:
                self._thread_in_msg_publisher.stop()
            self._thread_in_msg_publisher = None
            self._started = False

    def get_last_device_log_time(self, device_id: int):
        return self.device_log.get(device_id)

    def send(self, id: int, data: List[int]):
        """Send a message"""
        if self.is_started:
            msg = can.Message(arbitration_id=id, data=data, is_extended_id=False)
            self._dev_can.send(msg)

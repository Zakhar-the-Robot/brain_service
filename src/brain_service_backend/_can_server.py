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
import can


class CanServer:
    CANBUS_SERVICE_PORT = 5556
    CANBUS_SERVICE_MSG_RCV_TOPIC = "can_rcv"
    
    def __init__(self):
        self._log = new_logger(name="CanServer")
        self._thread_msg_publisher = None  # type: Union[ZmqPublisherThread, None]
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

    @property
    def is_stopped(self):
        return not self._started

    @property
    def is_started(self):
        return self._started

    def start(self):
        self._dev_can = can.interface.Bus(channel='can0', bustype='socketcan')
        if self.is_stopped:
            self._thread_msg_publisher = ZmqPublisherThread(port=self.CANBUS_SERVICE_PORT,
                                                            topic=self.CANBUS_SERVICE_MSG_RCV_TOPIC,
                                                            publish_callback=self._callback_publisher,
                                                            thread_name="CanServer thread",
                                                            publishing_freq_hz=0)
            self._thread_msg_publisher.start(log_level=LOG_LEVEL.INFO)
            self._started = True
        else:
            self._log.warning("Already started")

    def stop(self):
        if self.is_started:
            if self._thread_msg_publisher:
                self._thread_msg_publisher.stop()
            self._thread_msg_publisher = None
            self._started = False

    def get_last_device_log_time(self, device_id: int):
        return self.device_log.get(device_id)

    def send(self, id: int, data: List[int]):
        """Send a message"""
        if self.is_started:
            msg = can.Message(arbitration_id=id, data=data, is_extended_id=False)
            self._dev_can.send(msg)

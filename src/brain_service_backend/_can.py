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
from collections import deque
from typing import Dict, List, Union
from brain_pycore.zmq import (ZmqPublisherThread, ZmqSubscriberThread, ZmqServerThread, ZmqClientThread)
from brain_pycore.logging import new_logger, LOG_LEVEL
import can

CANBUS_SERVICE_PORT = 5556
CANBUS_SERVICE_MSG_RCV_TOPIC = "Can_rcv"


class CanBus:
    def __init__(self):
        self._started = False
        self._dev_can = None
        self._log = new_logger(name="Can sub-service")
        self._thread_msg_publisher = None  # type: Union[ZmqPublisherThread, None]
        self._device_log = {}  # type: Dict[int,datetime]
        self._messages = None  # type: Union[deque, None]

    def _canbus_listener(self):
        # print("CAN Listener start")
        msg = self._dev_can.recv()  # type: Union[can.Message, None]
        if msg:
            id = (msg.arbitration_id >> 8) & 0xF
            now = datetime.now()
            # print(f"[Can Message] Time: {now}, Id: {hex(id)}")
            if id:
                self._device_log[id] = now
            if self._messages is None:
                raise RuntimeError  # inticates that there was some logical mistake earliear.
                # This should not happen.
        msg_str = "{"+  f"'id': '{msg.arbitration_id}', 'data': '{msg.data}'" + "}"
        return msg_str

    @property
    def is_stopped(self):
        return not self._started

    @property
    def is_started(self):
        return self._started

    def start(self, max_messages: int = 0):
        self._dev_can = can.interface.Bus(channel='can0', bustype='socketcan')
        if self.is_stopped:
            if max_messages:
                self._messages = deque(maxlen=max_messages)
            else:
                self._messages = deque()
            self._thread_msg_publisher = ZmqPublisherThread(port=CANBUS_SERVICE_PORT, 
                                                            topic=CANBUS_SERVICE_MSG_RCV_TOPIC,
                                                            get_string_func=self._canbus_listener,
                                                            thread_name="Can sub-service thread")
            self._thread_msg_publisher.start()
            self._started = True
        else:
            print("Already started")

    def stop(self):
        if self.is_started:
            if self._thread_msg_publisher:
                self._thread_msg_publisher.stop()
            self._thread_msg_publisher = None
            self._started = False

    def get_last_device_log_time(self, device_id: int):
        return self._device_log.get(device_id)

    def get(self):
        """Get the last message"""
        if self._messages:
            return self._messages.pop()
        else:
            return None

    def send(self, id: int, data: List[int]):
        """Send a message"""
        if self.is_started:
            msg = can.Message(
                arbitration_id=id, 
                data=data, 
                is_extended_id=False
                )
            self._dev_can.send(msg)

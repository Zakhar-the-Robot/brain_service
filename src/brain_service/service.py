#!/usr/bin/env python3
from logging import DEBUG, INFO, WARNING
import sys
from time import sleep

# SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append("/zakhar/python_packages")
from brain_pycore.can import canbus


from brain_pycore.logging import log
from brain_service_backend import ZakharServiceBackend
from brain_service_frontend import ZakharServiceFrontend

def start():
    log.info("Service is starting...")
    canbus.start()  # TODO not sure, maybe canbus should be started from another place
    back = ZakharServiceBackend(update_period_ms=2000, no_connection=False, log_level=DEBUG)
    front = ZakharServiceFrontend(log_level=DEBUG)
    while 1:
        print("hello")
        sleep(60)  # MAGIC: pass here does not allow CANbus to start

# TODO Replace bash scripts with arguments for this script (sudo python service.py install)
if __name__ == "__main__":
    start()

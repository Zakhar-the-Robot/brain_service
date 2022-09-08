#!/usr/bin/env python3
import sys
sys.path.append("/zakhar/python_packages")

from logging import DEBUG, INFO, WARNING
from time import sleep

from brain_pycore.logging import log
from brain_service_backend import ZakharServiceBackend


if __name__ == "__main__":
    log.info("Backend Service is starting...")
    backend = ZakharServiceBackend(no_connection=False, log_level=DEBUG)
    backend.start()
    while 1:
        sleep(60)  # MAGIC: pass here does not allow CANbus to start

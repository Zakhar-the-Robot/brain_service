#!/usr/bin/env python3
from time import sleep
import sys

sys.path.append("/zakhar/python_packages")

from brain_pycore.logging import log, LOG_LEVEL
from brain_service_display import ServiceDisplay

if __name__ == "__main__":
    log.info("Display Service is starting...")
    front = ServiceDisplay(log_level=LOG_LEVEL.DEBUG)
    front.start()
    while 1:
        sleep(60)

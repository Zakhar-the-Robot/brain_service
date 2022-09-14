#!/usr/bin/env python3
from brain_service_frontend import ZakharServiceFrontend
from brain_pycore.logging import log, LOG_LEVEL
from time import sleep
import sys

sys.path.append("/zakhar/python_packages")


if __name__ == "__main__":
    log.info("Frontend Service is starting...")
    front = ZakharServiceFrontend(log_level=LOG_LEVEL.DEBUG)
    front.start()
    while 1:
        sleep(60)

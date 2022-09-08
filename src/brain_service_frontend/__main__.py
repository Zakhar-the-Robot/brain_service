#!/usr/bin/env python3
import sys
sys.path.append("/zakhar/python_packages")

from logging import DEBUG, INFO, WARNING
from time import sleep

from brain_pycore.logging import log
from brain_service_frontend import ZakharServiceFrontend


if __name__ == "__main__":
    log.info("Frontend Service is starting...")
    front = ZakharServiceFrontend(log_level=DEBUG)
    front.start()
    while 1:
        sleep(60)

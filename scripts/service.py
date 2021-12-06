#!/usr/bin/env python3
from logging import DEBUG, INFO, WARNING
import sys
import os
from time import sleep

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(SCRIPT_PATH + "/../python_packages")

from service_backend import ZakharServiceBackend
from service_frontend import ZakharServiceFrontend

def start():
    back = ZakharServiceBackend(update_period_ms=2000, no_connection=False, log_level=DEBUG)
    front = ZakharServiceFrontend(log_level=DEBUG)
    while 1:
        sleep(60)  # MAGIC: pass here does not allow can to start

# TODO Replace bash scripts with arguments for this script (sudo python service.py install)
if __name__ == "__main__":
    start()

#!/usr/bin/env python3
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

from time import sleep
import sys

sys.path.append("/zakhar/python_packages")
from brain_pycore.logging import log, LOG_LEVEL
from . import ZakharService

if __name__ == "__main__":
    log.info("Brain Service is starting...")
    backend = ZakharService(no_connection=False, 
                            log_level=LOG_LEVEL.DEBUG)
    backend.start()
    while 1:
        sleep(60)  # MAGIC: pass here does not allow CANbus to start

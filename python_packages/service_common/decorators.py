#!/usr/bin/env python3
# *************************************************************************
#
# Copyright (c) 2021 Andrei Gramakov. All rights reserved.
#
# This file is licensed under the terms of the MIT license.
# For a copy, see: https://opensource.org/licenses/MIT
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************

from service_common.common_types import Status
from service_common.internal import is_zakhar_environment


def zakhar_only_bool(func):
    def d(*args, **kwargs):
        if not is_zakhar_environment():
            return False
        return func(*args, **kwargs)

    return d


def zakhar_only_void(func):
    def d(*args, **kwargs):
        if not is_zakhar_environment():
            return
        func(*args, **kwargs)

    return d


def zakhar_only_str(func):
    def d(*args, **kwargs):
        if not is_zakhar_environment():
            return ""
        func(*args, **kwargs)

    return d


def zakhar_only_status(func):
    def d(*args, **kwargs):
        if not is_zakhar_environment():
            return Status.NA
        return func(*args, **kwargs)

    return d

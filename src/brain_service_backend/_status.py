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


class StatusClass(object):
    def update(self):
        raise NotImplementedError

    def __repr__(self) -> str:
        return str(vars(self))

    def __str__(self) -> str:
        return str(vars(self))

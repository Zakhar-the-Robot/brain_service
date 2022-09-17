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
from pathlib import Path

THIS_MODULE_PATH = Path(__file__).resolve().parent

PATH_ZK_CMDLINE = THIS_MODULE_PATH / "cmdline.txt"
PATH_ZK_CONFIG = THIS_MODULE_PATH / "config.txt"
PATH_RPI_CMDLINE = Path("/boot/cmdline.txt")
PATH_RPI_CONFIG = Path("/boot/config.txt")


class Files:
    @staticmethod
    def _get_content(src: Path):
        with src.open(mode='r') as f:
            return f.read()

    @classmethod
    def write_file_to_file(cls, src: Path, dst: Path, attach: bool = False):
        content = cls._get_content(src)
        if attach:
            w_mode = "a"
        else:
            w_mode = "w"
        with dst.open(mode=w_mode) as f:
            f.write(content)

    @classmethod
    def compare(cls, src: Path, dst: Path):
        return cls._get_content(src) == cls._get_content(dst)

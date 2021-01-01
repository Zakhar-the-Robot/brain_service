import os
import psutil
from subprocess import check_output
from .luma_ssd1306_mod import show_l, show_mm, show_sl
from zakhar_pycore.i2c import cmd
from zakhar_pycore.constants import ADDR
from time import sleep


def _is_service_active(name) -> bool:
    if os.system('systemctl is-active --quiet %s' % name):
        return False
    else:
        return True


def _is_process_exists(name) -> bool:
    return name in (p.name() for p in psutil.process_iter())


def check_ssh() -> bool:
    return _is_service_active("sshd")


def check_ros() -> bool:
    return _is_process_exists("roscore")


def check_face(show_error: bool = False) -> bool:
    try:
        cmd(ADDR.I2C.FACE, 0xFF)
        return True
    except OSError:
        if show_error:
            show_mm("Error!", "Face not found")
            sleep(1)
        return False


def check_sensors(show_error: bool = False) -> bool:
    try:
        cmd(ADDR.I2C.SENSORS, 0xFF)
        return True
    except OSError:
        if show_error:
            show_mm("Error!", "Sensors not found")
            sleep(1)
        return False


def check_motors(show_error: bool = False) -> bool:
    try:
        cmd(ADDR.I2C.MOTORS, 0xFF)
        return True
    except OSError:
        if show_error:
            show_mm("Error!", "Motors not found")
            sleep(1)
        return False


def check_network() -> bool:
    wifi_ip = check_output(['hostname', '-I'])
    if wifi_ip is not None:
        return True
    else:
        return False


if __name__ == "__main__":
    print("Start")
    print(check_network())

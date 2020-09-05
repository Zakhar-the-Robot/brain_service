import os
import psutil
import socket
from subprocess import check_output


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


def check_network() -> bool:
    wifi_ip = check_output(['hostname', '-I'])
    if wifi_ip is not None:
        return True
    else:
        return False


if __name__ == "__main__":
    print("Start")
    print(check_network())

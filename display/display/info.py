import socket
import ipaddress
import sys
from typing import Tuple
from subprocess import check_output


def get_net() -> Tuple[str, str]:
    hostname = socket.gethostname()
    ip = check_output(['hostname', '--all-ip-addresses']).decode(sys.stdout.encoding)
    ip = ip.strip("\n").strip()
    return (hostname, ip)


if __name__ == "__main__":
    print(get_net())
    # print()

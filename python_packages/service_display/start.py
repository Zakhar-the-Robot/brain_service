from .checks import check_face, check_motors, check_network, check_ros, check_sensors, check_ssh
from .info import get_net
from .luma_ssd1306_mod import show_l, show_mm, show_sl
from time import sleep


def start():
    show_l("   Hello", wait_sec=1)
    show_l("I am Zakhar", wait_sec=2)
    check_face(show_error=True)
    check_motors(show_error=True)
    check_sensors(show_error=True)

    show_sl("waiting for...", "network")
    while not check_network():
        sleep(.1)

    show_sl("waiting for...", "ssh")
    while not check_ssh():
        sleep(.1)

    while True:
        net_info = get_net()
        show_mm("Host: %s" % net_info[0], "IP: %s" % net_info[1], wait_sec=1)
        if (check_ros()):
            show_mm("roscore is active", "skip device check", wait_sec=5)
        else:
            f = "x"
            m = "x"
            s = "x"
            if check_face():
                f = "v"
            if check_motors():
                m = "v"
            if check_sensors():
                s = "v"
            show_mm("Devices:", " [%s]f   [%s]m   [%s]s" % (f, m, s), wait_sec=3)

        show_mm("zakhar.agramakov.me", "    GPLv3 (c) 2020", wait_sec=1)


if __name__ == "__main__":
    start()

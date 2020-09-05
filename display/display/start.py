from .checks import check_network, check_ros, check_ssh
from .info import get_net
from .luma_ssd1306_mod import show_l, show_mm, show_sl
from zakhar_pycore.zakhar__i2c import i2c_write_byte_data

from time import sleep
# draw.text((0, 0), "Example Text", font=FontTemp)

ADDR_MOTORS = 0x2a  # bus address
ADDR_EYE = 0x2b
ADDR_FACE = 0x2c
CMD_CALM = 0x30
CMD_BLINK = 0x31
CMD_ANGRY = 0x32
CMD_HAPPY = 0x33
CMD_SAD = 0x34

def main():
    show_l("   Hello")
    sleep(1)
    show_l("I am Zakhar")
    sleep(2)
    try:
        i2c_write_byte_data(ADDR_FACE, 0, CMD_CALM)  # wake up
    except OSError:
        show_mm("Error!", "Face not found")
        sleep(1)
    try:
        i2c_write_byte_data(ADDR_EYE, 0, 0xFF)  # wake up
    except OSError:
        show_mm("Error!", "Sensors not found")
        sleep(1)
    try:
        i2c_write_byte_data(ADDR_MOTORS, 0, 0xFF)  # wake up
    except OSError:
        show_mm("Error!", "Motors not found")
        sleep(1)
    show_sl("waiting for...", "network")
    while not check_network():
        sleep(.1)

    show_sl("waiting for...", "ssh")
    while not check_ssh():
        sleep(.1)

    show_sl("waiting for...", "roscore")
    while not check_ros():
        sleep(.1)

    net_info = get_net()
    while True:
        show_mm("Host: %s" % net_info[0], "IP: %s" % net_info[1])
        sleep(2)
        show_mm("zakhar.agramakov.me", "    GPLv3 (c) 2020")
        sleep(5)


if __name__ == "__main__":
    main()

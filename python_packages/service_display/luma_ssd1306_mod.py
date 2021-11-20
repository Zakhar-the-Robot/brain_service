from luma.core.device import device
import luma.core.error
import luma.core.framebuffer
import luma.oled.const
from luma.core.render import canvas
from luma.core.interface.serial import i2c
from PIL import ImageFont
from time import sleep
from .fonts import FONT_LONG_PIXEL_7


class ssd1306_mod(device):
    """
    Serial interface to a monochrome SSD1306 OLED display.

    On creation, an initialization sequence is pumped to the display
    to properly configure it. Further control commands can then be called to
    affect the brightness and other settings.

    :param serial_interface: The serial interface (usually a
        :py:class:`luma.core.interface.serial.i2c` instance) to delegate sending
        data and commands through.
    :param width: The number of horizontal pixels (optional, defaults to 128).
    :type width: int
    :param height: The number of vertical pixels (optional, defaults to 64).
    :type height: int
    :param rotate: An integer value of 0 (default), 1, 2 or 3 only, where 0 is
        no rotation, 1 is rotate 90° clockwise, 2 is 180° rotation and 3
        represents 270° rotation.
    :type rotate: int
    """
    def __init__(self, serial_interface=None, width=128, height=64, rotate=0, **kwargs):
        super(ssd1306_mod, self).__init__(luma.oled.const.ssd1306, serial_interface)
        self.capabilities(width, height, rotate)

        # Supported modes
        settings = {
            (128, 64): dict(multiplex=0x3F, displayclockdiv=0x80, compins=0x12),
            (128, 32): dict(multiplex=0x1F, displayclockdiv=0x80, compins=0x02),
            (96, 16): dict(multiplex=0x0F, displayclockdiv=0x60, compins=0x02),
            (64, 48): dict(multiplex=0x2F, displayclockdiv=0x80, compins=0x12),
            (64, 32): dict(multiplex=0x1F, displayclockdiv=0x80, compins=0x12)
        }.get((width, height))

        if settings is None:
            raise luma.core.error.DeviceDisplayModeError("Unsupported display mode: {0} x {1}".format(width, height))

        self._pages = height // 8
        self._mask = [1 << (i // width) % 8 for i in range(width * height)]
        self._offsets = [(width * (i // (width * 8))) + (i % width) for i in range(width * height)]
        self._colstart = (0x80 - self._w) // 2
        self._colend = self._colstart + self._w

        self.command(self._const.DISPLAYOFF, self._const.SETDISPLAYCLOCKDIV, settings['displayclockdiv'],
                     self._const.SETMULTIPLEX, settings['multiplex'], self._const.SETDISPLAYOFFSET, 0x00,
                     self._const.SETSTARTLINE, self._const.CHARGEPUMP, 0x14, self._const.MEMORYMODE, 0x00,
                     self._const.SETSEGMENTREMAP, self._const.COMSCANDEC, self._const.SETCOMPINS, settings['compins'],
                     self._const.SETPRECHARGE, 0xF1, self._const.SETVCOMDETECT, 0x40, self._const.DISPLAYALLON_RESUME,
                     self._const.NORMALDISPLAY)

        self.contrast(0xCF)
        self.clear()
        self.show()

    def display(self, image):
        """
        Takes a 1-bit :py:mod:`PIL.Image` and dumps it to the SH1106
        OLED display.

        :param image: Image to display.
        :type image: :py:mod:`PIL.Image`
        """
        assert (image.mode == self.mode)
        assert (image.size == self.size)

        image = self.preprocess(image)

        set_page_address = 0xB0
        image_data = image.getdata()
        pixels_per_page = self.width * 8
        buf = bytearray(self.width)

        for y in range(0, int(self._pages * pixels_per_page), pixels_per_page):
            self.command(set_page_address, 0x00, 0x10)
            set_page_address += 1
            offsets = [y + self.width * i for i in range(8)]

            for x in range(self.width):
                buf[x] = \
                    (image_data[x + offsets[0]] and 0x01) | \
                    (image_data[x + offsets[1]] and 0x02) | \
                    (image_data[x + offsets[2]] and 0x04) | \
                    (image_data[x + offsets[3]] and 0x08) | \
                    (image_data[x + offsets[4]] and 0x10) | \
                    (image_data[x + offsets[5]] and 0x20) | \
                    (image_data[x + offsets[6]] and 0x40) | \
                    (image_data[x + offsets[7]] and 0x80)

            self.data(list(buf))


bus = i2c(port=1, address=0x3C)
oled = ssd1306_mod(bus, rotate=2, height=32)
fnt_small = ImageFont.truetype(FONT_LONG_PIXEL_7, 8)
fnt_medium = ImageFont.truetype(FONT_LONG_PIXEL_7, 12)
fnt_big = ImageFont.truetype(FONT_LONG_PIXEL_7, 18)


def show_l(text, wait_sec: int = 0):
    with canvas(oled) as draw:
        draw.text((1, 6), text, fill="white", font=fnt_big)
    sleep(wait_sec)


def show_sl(text_line1, text_line2="", wait_sec: int = 0):
    with canvas(oled) as draw:
        draw.text((1, 3), text_line1, fill="white", font=fnt_small)
        draw.text((1, 18), text_line2, fill="white", font=fnt_big)
    sleep(wait_sec)


def show_mm(text_line1, text_line2="", wait_sec: int = 0):
    with canvas(oled) as draw:
        draw.text((1, 4), text_line1, fill="white", font=fnt_medium)
        draw.text((1, 22), text_line2, fill="white", font=fnt_medium)
    sleep(wait_sec)


def show_clear():
    oled.clear()

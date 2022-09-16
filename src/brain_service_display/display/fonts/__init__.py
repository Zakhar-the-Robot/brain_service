import os
from PIL import ImageFont


FONT_LONG_PIXEL_7_PATH = os.path.dirname(os.path.realpath(__file__)) + "/long_pixel-7.ttf"

FONT_LONG_PIXEL_7_SMALL = ImageFont.truetype(FONT_LONG_PIXEL_7_PATH, 8)
FONT_LONG_PIXEL_7_MEDIUM = ImageFont.truetype(FONT_LONG_PIXEL_7_PATH, 12)
FONT_LONG_PIXEL_7_LARGE = ImageFont.truetype(FONT_LONG_PIXEL_7_PATH, 18)

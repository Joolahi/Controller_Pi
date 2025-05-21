import time
import board
import busio
import digitalio
import displayio
from adafruit_displayio_ssd1351 import SSD1351
from PIL import Image, ImageDraw, ImageFont
import adafruit_sht31d

displayio.release_displays()

# I2C (SHT35)
i2c = busio.I2C(board.SCL, board.SDA)
sht = adafruit_sht31d.SHT31D(i2c, address=0x45)

# SPI (OLED)
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D25)
reset = digitalio.DigitalInOut(board.D24)

display_bus = displayio.FourWire(spi, command=dc, chip_select=cs, reset=reset)
display = SSD1351(display_bus, width=128, height=128)

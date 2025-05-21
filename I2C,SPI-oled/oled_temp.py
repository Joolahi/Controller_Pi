import time
import board
import busio
import digitalio
import adafruit_sht31d
import adafruit_ssd1351
from PIL import Image, ImageDraw, ImageFont

# SHT35 (I2C)
i2c = busio.I2C(board.SCL, board.SDA)
sht = adafruit_sht31d.SHT31D(i2c, address=0x45)

# OLED (SPI)
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.CE0)  # GPIO8
dc = digitalio.DigitalInOut(board.D25)  # GPIO25
reset = digitalio.DigitalInOut(board.D24)  # GPIO24

display = adafruit_ssd1351.SSD1351(spi, cs=cs, dc=dc, rst=reset, width=128, height=128)

font = ImageFont.load_default()

while True:
    temp = sht.temperature
    humidity = sht.relative_humidity

    image = Image.new("RGB", (128, 128))
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, 128, 128), fill=(0, 0, 0)) # Clear the screen
    draw.text((10, 30), f"Temp: {temp:.1f} C", font=font, fill=(255, 255, 255))
    draw.text((10, 60), f"Hum:  {humidity:.1f} %", font=font, fill=(255, 255, 255))

    display.image(image)
    time.sleep(2)

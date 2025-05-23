import board
import busio
import displayio
from adafruit_ssd1327 import SSD1327
from adafruit_display_text import label
from adafruit_display_text import wrap_text_to_lines
import terminalio
import time
import adafruit_sht31d

# Release any previous displays
displayio.release_displays()

# Setup SPI for OLED
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
display_bus = displayio.FourWire(spi, command=board.D25, chip_select=board.CE0, reset=board.D24)
display = SSD1327(display_bus, width=128, height=128)

# Setup I2C for sensor
i2c = busio.I2C(scl=board.SCL, sda=board.SDA)
sensor = adafruit_sht31d.SHT31D(i2c, address=0x45)

# Create display group
main_group = displayio.Group()
display.root_group = main_group

# Background
bitmap = displayio.Bitmap(128, 128, 1)
palette = displayio.Palette(1)
palette[0] = 0x000000
bg_sprite = displayio.TileGrid(bitmap, pixel_shader=palette)
main_group.append(bg_sprite)

# Large font (use built-in font for now)
font = terminalio.FONT

# Temperature Label
temp_label = label.Label(font, text="Temp:", x=10, y=40)
main_group.append(temp_label)

temp_value = label.Label(font, text="--.- °C", x=60, y=40)
main_group.append(temp_value)

# Humidity Label
hum_label = label.Label(font, text="Hum:", x=10, y=70)
main_group.append(hum_label)

hum_value = label.Label(font, text="--.- %", x=60, y=70)
main_group.append(hum_value)

# Update loop
while True:
    temperature = sensor.temperature
    humidity = sensor.relative_humidity

    temp_value.text = f"{temperature:.1f} °C"
    hum_value.text = f"{humidity:.1f} %"

    time.sleep(2)

import board
import busio
import displayio
import terminalio
from adafruit_ssd1327 import SSD1327
from adafruit_display_text import label
import adafruit_sht31d
import time
import requests
from dotenv import load_dotenv
import os 

load_dotenv()
FIREBASE_URL = os.getenv("FIREBASE_URL") 
# Release previous displays
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
palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xFFFFFF
bg_sprite = displayio.TileGrid(bitmap, pixel_shader=palette)
main_group.append(bg_sprite)

# Labels
temp_label = label.Label(terminalio.FONT, text="Temp:", x=0, y=30)
hum_label = label.Label(terminalio.FONT, text="Hum: ", x=0, y=60)
main_group.append(temp_label)
main_group.append(hum_label)

# Dynamic text
temp_text = label.Label(terminalio.FONT, text="--.- °C", x=50, y=30)
hum_text = label.Label(terminalio.FONT, text="--.- %", x=50, y=60)
main_group.append(temp_text)
main_group.append(hum_text)

# Bar outline boxes
bar_width = 70
bar_height = 10

# Create two rectangles for temp/hum bars
temp_bar = displayio.Bitmap(bar_width, bar_height, 1)
hum_bar = displayio.Bitmap(bar_width, bar_height, 1)

temp_bar_tile = displayio.TileGrid(temp_bar, pixel_shader=palette, x=50, y=40)
hum_bar_tile = displayio.TileGrid(hum_bar, pixel_shader=palette, x=50, y=70)

main_group.append(temp_bar_tile)
main_group.append(hum_bar_tile)

# Bar fill helpers
def update_bar(bitmap, value, max_value):
    fill = int((value / max_value) * bitmap.width)
    for x in range(bitmap.width):
        for y in range(bitmap.height):
            bitmap[x, y] = 1 if x < fill else 0

# Send data to Firebase
def send_to_firebase(temp, hum):
    data = {"temperature":temp, "humidity": hum}
    try:
        response = requests.put(FIREBASE_URL, json=data, timeout=5)
        print(f"FIREBASE status: {response.status_code}")
    except Exception as e:
        print("Firebase error:", e)

# Main loop
while True:
    temperature = sensor.temperature
    humidity = sensor.relative_humidity

    temp_text.text = f"{temperature:.1f} °C"
    hum_text.text = f"{humidity:.1f} %"

    update_bar(temp_bar, temperature, 50)  # Scale: 0–50°C
    update_bar(hum_bar, humidity, 100)     # Scale: 0–100%
    send_to_firebase(temperature, humidity)

    time.sleep(6)

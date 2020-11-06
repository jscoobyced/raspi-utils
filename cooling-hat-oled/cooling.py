import subprocess
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
import Adafruit_SSD1306
import Adafruit_GPIO.I2C as I2C

import time
import os
import smbus
bus = smbus.SMBus(1)

hat_addr = 0x0d
fan_reg = 0x08
fan_state = 3
count = 0
TEMP_HIGH = 55
TEMP_MEDIUM = 53
TEMP_LOW = 48

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)


def setFanSpeed(speed):
    bus.write_byte_data(hat_addr, fan_reg, speed & 0xff)


def setRGB(r, g, b):
    bus.write_byte_data(hat_addr, 0x00, 0xff)
    bus.write_byte_data(hat_addr, 0x01, r & 0xff)
    bus.write_byte_data(hat_addr, 0x02, g & 0xff)
    bus.write_byte_data(hat_addr, 0x03, b & 0xff)


def getCPULoadRate():
    f1 = os.popen("cat /proc/stat", 'r')
    stat1 = f1.readline()
    count = 10
    data_1 = []
    for i in range(count):
        data_1.append(int(stat1.split(' ')[i+2]))
    total_1 = data_1[0]+data_1[1]+data_1[2]+data_1[3] + \
        data_1[4]+data_1[5]+data_1[6]+data_1[7]+data_1[8]+data_1[9]
    idle_1 = data_1[3]

    time.sleep(1)

    f2 = os.popen("cat /proc/stat", 'r')
    stat2 = f2.readline()
    data_2 = []
    for i in range(count):
        data_2.append(int(stat2.split(' ')[i+2]))
    total_2 = data_2[0]+data_2[1]+data_2[2]+data_2[3] + \
        data_2[4]+data_2[5]+data_2[6]+data_2[7]+data_2[8]+data_2[9]
    idle_2 = data_2[3]

    total = int(total_2-total_1)
    idle = int(idle_2-idle_1)
    usage = int(total-idle)
    usageRate = int(float(usage * 100 / total))
    return "CPU:"+str(usageRate)+"%"


def setOLEDshow():
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #cmd = "top -bn1 | grep load | awk '{printf \"CPU:%.0f%%\", $(NF-2)*100}'"
    #CPU = subprocess.check_output(cmd, shell = True)
    CPU = getCPULoadRate()

    cmd = os.popen('./vcgencmd measure_temp').readline()
    CPU_TEMP = cmd.replace("temp=", "Temp:").replace("'C\n", "C")
    global g_temp
    g_temp = float(cmd.replace("temp=", "").replace("'C\n", ""))

    cmd = "free -m | awk 'NR==2{printf \"RAM:%s/%s MB \", $2-$3,$2}'"
    MemUsage = subprocess.check_output(cmd, shell=True)

    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk:%d/%dMB\", ($2-$3)*1024,$2*1024}'"
    Disk = subprocess.check_output(cmd, shell=True)

    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True)

    # Write two lines of text.

    draw.text((x, top), str(CPU), font=font, fill=255)
    draw.text((x+56, top), str(CPU_TEMP), font=font, fill=255)
    draw.text((x, top+8), str(MemUsage),  font=font, fill=255)
    draw.text((x, top+16), str(Disk),  font=font, fill=255)
    draw.text((x, top+24), "wlan0:" + str(IP),  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)


setFanSpeed(0x00)

while True:
    setOLEDshow()
    if g_temp >= TEMP_HIGH:
        if fan_state != 2:
            setFanSpeed(0x02)
            fan_state = 2
            setRGB(0xff, 0x00, 0x00)
    if g_temp > TEMP_LOW and g_temp <= TEMP_MEDIUM:
        if fan_state != 1:
            setFanSpeed(0x01)
            fan_state = 1
            setRGB(0x00, 0xff, 0x00)
    if g_temp <= TEMP_LOW:
        if fan_state != 0:
            setFanSpeed(0x00)
            fan_state = 0
            setRGB(0x00, 0x00, 0xff)

    count += 1
    time.sleep(2)

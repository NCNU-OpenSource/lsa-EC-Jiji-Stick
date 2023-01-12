# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 22:52:44 2023

@author: user
"""

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the TCS34725 color sensor.
# Will detect the color from the sensor and print it out every second.
import time
import board
import adafruit_tcs34725
import os

import asyncio
import websockets

async def sendCmd(uri, msg):
    async with websockets.connect(uri) as websocket:
        await websocket.send( msg )


# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a m>
sensor = adafruit_tcs34725.TCS34725(i2c)

# Change sensor integration time to values between 2.4 and 614.4 milliseconds
# sensor.integration_time = 150

# Change sensor gain to 1, 4, 16, or 60
# sensor.gain = 4

# Main loop reading color and printing it every second.
def action1():
    a1 = "mplayer /home/pi/Music/'HOT HOT HOT - Gaming Sound Effect (HD)-vFrNxJJoB768.mp3'"
    os.system(a1)

def action2():
    a2 = "mplayer /home/pi/Music/Yee-q6EoRBvdVPQ.mp3"
    os.system(a2)

def action3():
    a3 = "mplayer /home/pi/Music/'TADAAH - Gaming Sound Effect (HD)-jLtbFWJm9_M.mp3'"
    os.system(a3)

def action4():
    a4 = "mplayer /home/pi/Music/'20TH CENTURYEE YEE-OTk6m3U54po.mp3'"
    os.system(a4)

asyncio.get_event_loop().run_until_complete(
    sendCmd('ws://192.168.0.140:4545', 'Start'))

while True:
    # Raw data from the sensor in a 4-tuple of red, green, blue, clear light co>
    # print(sensor.color_raw)

    color = sensor.color
    color_rgb = sensor.color_rgb_bytes
    print(
        "RGB color as 8 bits per channel int: {0:02X} or as 3-tuple: {1}".format(
            color, color_rgb
        )
    )
    red = color_rgb[0]
    green = color_rgb[1]
    blue = color_rgb[2]

    print("red: {} , green: {}, blue: {}".format(red,green,blue))

    asyncio.get_event_loop().run_until_complete(
           sendCmd('ws://192.168.0.140:4545', "{},{},{}".format(red,green,blue)))

    # Read the color temperature and lux of the sensor too.
    temp = sensor.color_temperature
    lux = sensor.lux
    print("Temperature: {0}K Lux: {1}\n".format(temp, lux))
    # Delay for a second and repeat.
    time.sleep(0.2)
    
    # blue
    if ((red==16 and green==16 and blue==16) or (red==45 and green==45 and blue==45)):
        action1()
    # red
    if ((red>=125 and red <=184) and green==1 and blue==1):
        asyncio.get_event_loop().run_until_complete(
           sendCmd('ws://192.168.0.140:4545', 'Stop'))
        action4()
        exit()
    # yellow
    if ((red>50 and red<70) and (green>10 and green<20) and (blue>=1 and blue<=3)):
        action2()
        
    # green
    if ((red>3 and red<25) and (green>=22 and green<=80) and (blue>3 and blue<=30)):
        action3()

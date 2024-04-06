import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
from digitalio import DigitalInOut, Direction

from time import sleep

import wifi
import socketpool

import adafruit_requests
from adafruit_hashlib import sha1
from json import dumps
import ssl
from base64 import b64encode
import gc


WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
HVV_USER = "YOUR_HVV_API_USERNAME"
HVV_PASSWORD = "YOUR_HVV_API_PASSWORD"

bit_depth_value = 2
base_width = 64
base_height = 32
chain_across = 1
tile_down = 2
serpentine_value = True

width_value = base_width * chain_across
height_value = base_height * tile_down

# If there was a display before (protomatter, LCD, or E-paper), release it so
# we can create ours
displayio.release_displays()

# send register
R1 = DigitalInOut(board.GP2)
G1 = DigitalInOut(board.GP3)
B1 = DigitalInOut(board.GP4)
R2 = DigitalInOut(board.GP5)
G2 = DigitalInOut(board.GP8)
B2 = DigitalInOut(board.GP9)
CLK = DigitalInOut(board.GP11)
STB = DigitalInOut(board.GP12)
OE = DigitalInOut(board.GP13)

R1.direction = Direction.OUTPUT
G1.direction = Direction.OUTPUT
B1.direction = Direction.OUTPUT
R2.direction = Direction.OUTPUT
G2.direction = Direction.OUTPUT
B2.direction = Direction.OUTPUT
CLK.direction = Direction.OUTPUT
STB.direction = Direction.OUTPUT
OE.direction = Direction.OUTPUT

OE.value = True
STB.value = False
CLK.value = False

MaxLed = 64

c12 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
c13 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

for l in range(0, MaxLed):
    y = l % 16
    R1.value = False
    G1.value = False
    B1.value = False
    R2.value = False
    G2.value = False
    B2.value = False

    if c12[y] == 1:
        R1.value = True
        G1.value = True
        B1.value = True
        R2.value = True
        G2.value = True
        B2.value = True
    if l > (MaxLed - 12):
        STB.value = True
    else:
        STB.value = False
    CLK.value = True
    # time.sleep(0.000002)
    CLK.value = False
STB.value = False
CLK.value = False

for l in range(0, MaxLed):
    y = l % 16
    R1.value = False
    G1.value = False
    B1.value = False
    R2.value = False
    G2.value = False
    B2.value = False

    if c13[y] == 1:
        R1.value = True
        G1.value = True
        B1.value = True
        R2.value = True
        G2.value = True
        B2.value = True
    if l > (MaxLed - 13):
        STB.value = True
    else:
        STB.value = False
    CLK.value = True
    # time.sleep(0.000002)
    CLK.value = False
STB.value = False
CLK.value = False

R1.deinit()
G1.deinit()
B1.deinit()
R2.deinit()
G2.deinit()
B2.deinit()
CLK.deinit()
STB.deinit()
OE.deinit()

# This next call creates the RGB Matrix object itself. It has the given width
# and height. bit_depth can range from 1 to 6; higher numbers allow more color
# shades to be displayed, but increase memory usage and slow down your Python
# code. If you just want to show primary colors plus black and white, use 1.
# Otherwise, try 3, 4 and 5 to see which effect you like best.
#
# These lines are for the Feather M4 Express. If you're using a different board,
# check the guide to find the pins and wiring diagrams for your board.
# If you have a matrix with a different width or height, change that too.
# If you have a 16x32 display, try with just a single line of text.
matrix = rgbmatrix.RGBMatrix(
    width=width_value, height=height_value, bit_depth=bit_depth_value,
    rgb_pins=[board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
    addr_pins=[board.GP10, board.GP16, board.GP18, board.GP20],
    clock_pin=board.GP11, latch_pin=board.GP12, output_enable_pin=board.GP13,
    tile=tile_down, serpentine=serpentine_value,
    doublebuffer=False)

# Associate the RGB matrix with a Display so that we can use displayio features
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)

display.rotation = 0
#display.brightness = 0.0001


wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
pool = socketpool.SocketPool(wifi.radio)


### Request payload with your start station
payload = {
    "version": 55,
    "station": {
        "name": "Gruendgensstrasse (West)",
        "type": "STATION",
    },
    "time": {
        "date": "heute", "time": "jetzt"
    },
    "maxList": 10,
    "maxTimeOffset": 200,
    "useRealtime":"true",
}
SHA1 = sha1
def HMAC(k, m):
    SHA1_BLOCK_SIZE = 64
    KEY_BLOCK = k + (b'\0' * (SHA1_BLOCK_SIZE - len(k)))
    KEY_INNER = bytes((x ^ 0x36) for x in KEY_BLOCK)
    KEY_OUTER = bytes((x ^ 0x5C) for x in KEY_BLOCK)
    inner_message = KEY_INNER + m
    outer_message = KEY_OUTER + SHA1(inner_message).digest()
    return SHA1(outer_message)
sig = b64encode(HMAC(HVV_PASSWORD.encode("UTF-8"), dumps(payload).encode('UTF-8')).digest())
requests = adafruit_requests.Session(pool, ssl.create_default_context())
def get_departures(lines):
    currentline = 0
    req = requests.post('https://gti.geofox.de/gti/public/departureList', json=payload, headers={"geofox-auth-user":HVV_USER, "geofox-auth-signature":sig})
    input_dict = req.json()
    # In the following line you can add additional filtering like for directionId or line name. Just have a look at the input_dict json.
    output_dict = [x for x in input_dict['departures']]
    output_str = ""
    for key in output_dict:
        currentline += 1
        if (currentline > lines):
            break
        if (key['timeOffset'] < 0):
            continue
        output_str += '{:3}'.format(key['line']['name'])
        output_str += ": "+ str(key['timeOffset']) + "min\n"
    print(output_str)
    return output_str

# You can add more effects in this loop. For instance, maybe you want to set the
# color of each label to a different value.
while True:
    gc.collect()
    out_str = get_departures(4)
    label1 = adafruit_display_text.label.Label(
        terminalio.FONT,
        color=0xFF0044,
        line_spacing=0.7,
        text=out_str,
        anchor_point=(0, 0),
        anchored_position=(0, -2)
    )
    #0xFF0055
    display.show(label1)
    sleep(60)
    #scroll(line1)
    #display.refresh(minimum_frames_per_second=0)

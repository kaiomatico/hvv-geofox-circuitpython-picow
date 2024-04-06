# hvv-geofox-circuitpython-picow
Example of using the HVV Geofox public transport API on circuitpython microcontrollers and displaying it using a HUB75 LED Matrix (tested on Raspberry Pi Pico W).

## Showcase
![Showcase](showcase.jpeg?raw=true "Showcase")

## Parts
- Raspberry Pi Pico W with soldered headers: https://amzn.eu/d/13qviXV
- HUB75 RGB Matrix Adapter Board: https://amzn.eu/d/96GlWPC
- 64x32 RGB LED Matrix https://amzn.eu/d/fDSUKWO

## Prerequisites
You need to ask for API credentials here: https://www.hvv.de/de/fahrplaene/abruf-fahrplaninfos/datenabruf (click on API-Zugang beantragen, and explain your project in the e-mail)

## Installation
1. Install CircuitPython: https://circuitpython.org/board/raspberry_pi_pico_w/ (tested with version 8.2.10 from 2024-02-14)
2. Clone this repository and copy & paste it to your Raspberry Pi Pico W (except for showcase.jpeg)
3. Adjust your Wifi and API credentials in the code.py file
4. Have fun :tada: 

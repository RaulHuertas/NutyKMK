# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Print out the color data from ColorPackets.
# To use, start this program, and start the Adafruit Bluefruit LE Connect app.
# Connect, and then select colors on the Controller->Color Picker screen.

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet

# Only the packet classes that are imported will be known to Packet.
from adafruit_bluefruit_connect.color_packet import ColorPacket
import board 
import digitalio 
import time
led1 = digitalio.DigitalInOut(board.LED_RED)
led2 = digitalio.DigitalInOut(board.LED_GREEN)
led1.direction = digitalio.Direction.OUTPUT
led2.direction = digitalio.Direction.OUTPUT
ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)
ble.name = "Nuty labs test switches"


import keypad
import board

km = keypad.KeyMatrix(
    row_pins=(board.D1,board.D2,board.D3 ,board.D4,),
    column_pins= (board.NFC1,board.NFC2,board.D7,board.D8, board.D9,board.D10),
    columns_to_anodes=False,
)


    
 # Advertise when not connected.
ble.start_advertising(advertisement)

while True:
   
    

    event = km.events.get()
    if event:
        print(event)


    if not ble.connected:
        pass

    if ble.connected:
        packet = Packet.from_stream(uart_server)
        if isinstance(packet, ColorPacket):
            print(packet.color)

    time.sleep(0.5)
    
    print("lll")
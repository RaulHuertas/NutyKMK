
print("Starting on NML")

import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation
# from kmk.modules.splitBLE import SplitBLE, SplitSide 
from kmk.modules.split import Split, SplitSide, SplitType
import busio
#from snKeycodes import ESKeycodes
from kmk.extensions.media_keys import MediaKeys
from keyAssignations import assignKeys
from kmk.modules.layers import Layers
# from kmk.modules.mouse_keys import MouseKeys
from kmk.scanners.keypad import MatrixScanner


import board
from kmk.hid import HIDModes

from kmk.modules.power import Power

#col_pins = (board.P0_17,board.P0_20,board.P0_22,board.P0_24, board.P1_00,board.P0_11,)
col_pins = (board.D1,board.D2,board.D3,board.D4, board.D5,board.D6,)
row_pins = (board.NFC1, board.NFC2, board.D7,board.D8,)


diode_orientation = DiodeOrientation.ROW2COL
class MyKeyboard(KMKKeyboard):
    def __init__(self):
        # create and register the scanner
        self.matrix = MatrixScanner(
            # required arguments:
            column_pins=col_pins,
            row_pins=row_pins,
            # optional arguments with defaults:
                columns_to_anodes=diode_orientation,
            interval=0.020,  # Debounce time in floating point seconds
            max_events=64
        )               
keyboard = MyKeyboard()
keyboard.coord_mapping = [
    0,  1,  2,  3,  4,  5, 
    24, 25, 26, 27, 28, 29,                          
    6,  7,  8,  9, 10, 11,
    30, 31, 32, 33, 34, 35,
    12, 13, 14, 15, 16, 17,
    36, 37, 38, 39, 40, 41,
    18, 19, 20, 21, 22, 23,
    42, 43, 44, 45, 46, 47,
]


split = Split(
    split_side=SplitSide.LEFT,
    #split_side=None,
    split_type=SplitType.UART,
    split_target_left=False,
    data_pin = board.D9,#RX
    data_pin2 = board.D10,#TX
    uart_flip = False,
    debug_enabled = False
)

mediaKeys = MediaKeys()
mouseKeys = Layers()
layers = Layers()
power = Power()
keyboard.keymap = assignKeys()


keyboard.extensions = [
    mediaKeys
]
keyboard.modules = [
    split, 
    layers, 
    power,
    mouseKeys
    #keyboard.modules.append(holdtap),
]


keyboard.debug_enabled = False
#keyboard.powersave_enable()
print("Starting on NML now")
if __name__ == '__main__':
    #keyboard.go(hid_type=HIDModes.BLE )
    keyboard.go( )





print("Starting on SHIRIR")

import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.modules.split import Split, SplitSide,SplitType
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.layers import Layers
from kmk.modules.mouse_keys import MouseKeys
from kmk.scanners.keypad import MatrixScanner

from kmk.modules.pimoroni_trackball import Trackball

col_pins = (board.P0_31,board.P0_29,board.P0_02,board.P1_15, board.P1_13,board.P1_11,)
row_pins = (board.P0_10,board.P0_09,board.P1_07 ,board.P1_02,)

diode_orientation = DiodeOrientation.ROW2COL
class NutyKeyboard(KMKKeyboard):
    def __init__(self):
        # create and register the scanner
        self.matrix = MatrixScanner(
            # required arguments:
            column_pins=col_pins,
            row_pins=row_pins,
            # optional arguments with defaults:
            columns_to_anodes=diode_orientation,
            interval=0.020,  # Debounce time in floating point seconds
            max_events=2
        )
keyboard = NutyKeyboard()

keyboard.coord_mapping =  [
    0,  1,  2,  3,  4,  5, 
    24, 25, 26, 27, 28, 29,
    6,  7,  8,  9, 10, 11,
    30, 31, 32, 33, 34, 35,
    12, 13, 14, 15, 16, 17,
    36, 37, 38, 39, 40, 41,
    18, 19, 20, 21, 22, 23 ,
    42, 43, 44, 45, 46, 47,
]

split = Split(
    split_side=SplitSide.RIGHT,
    #split_side=None,
    split_type=SplitType.UART,
    split_target_left=False,
    data_pin = board.P1_04,#RX
    data_pin2 = board.P1_06,#TX
    uart_flip = False,
    debug_enabled = False
)

i2c = busio.I2C(scl=board.P0_06, sda=board.P0_08)

trackball = Trackball(
    i2c,
    angle_offset=270,
    
)
trackball.set_rgbw(200, 0, 255, 0)

keyboard.extensions.append(MediaKeys())
# keyboard.extensions.append(rgb)

keyboard.modules = [
    split, 
    Layers(), 
 #   power,
    MouseKeys(),
    trackball,
    #keyboard.modules.append(holdtap),
]

from keyAssignations import assignKeys
keyboard.keymap = assignKeys()
keyboard.debug_enabled = True
keyboard.powersave_pin = board.P0_13

if __name__ == '__main__':
    #keyboard.go(hid_type=HIDModes.BLE)
    keyboard.go()



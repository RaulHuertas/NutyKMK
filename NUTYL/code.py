
print("Starting on NML")

import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.modules.split import Split, SplitSide, SplitType
#from snKeycodes import ESKeycodes

from kmk.modules.layers import Layers
from kmk.scanners.keypad import MatrixScanner

from kmk.extensions.rgb import RGB


#col_pins = (board.P0_17,board.P0_20,board.P0_22,board.P0_24, board.P1_00,board.P0_11,)
col_pins = (board.D1,board.D2,board.D3,board.D4, board.D5,board.D6,)
row_pins = (board.NFC1, board.NFC2, board.D7,board.D8,)


class RGBController(RGB):
    
    def after_hid_send(self, sandbox):
        super().after_hid_send(sandbox)  # Critically important. Do not forget

    def during_bootup(self, keyboard):
        super().during_bootup(keyboard)

    def before_matrix_scan(self, keyboard):
        super().before_matrix_scan(keyboard)
        bLevel = self.br*0.8
        self.set_rgb((bLevel*0, bLevel, bLevel*0), 0)
        self.show() 
        
    def on_layer_change(self, layer):
        onComb = (self.br,self.br*0, self.br)
        offComb = (0, 0, 0)

        if layer == 0:
            self.set_rgb(offComb, 1)
            self.set_rgb(offComb, 2)
            self.set_rgb(offComb, 3)
            self.set_rgb(offComb, 4)
            self.set_rgb(offComb, 5)
        elif layer == 1:
            self.set_rgb(onComb, 1)
            self.set_rgb(offComb, 2)
            self.set_rgb(offComb, 3)
            self.set_rgb(offComb, 4)
            self.set_rgb(offComb, 5)
        elif layer == 2:
            self.set_rgb(onComb, 1)
            self.set_rgb(onComb, 2)
            self.set_rgb(offComb, 3)
            self.set_rgb(offComb, 4)
            self.set_rgb(offComb, 5)
        elif layer == 3:
            self.set_rgb(onComb, 1)
            self.set_rgb(onComb, 2)
            self.set_rgb(onComb, 3)
            self.set_rgb(offComb, 4)
            self.set_rgb(offComb, 5)
        self.show()

rgbController = RGBController(
        pixel_pin=board.D0, # GPIO pin of the status LED, or background RGB light
        num_pixels=6,                # one if status LED, more if background RGB light
        rgb_order=(1, 0, 2),
        hue_default=0,               # in range 0-255: 0/255-red, 85-green, 170-blue
        sat_default=0,
        val_default=0,
        )
rgbController.br = 3

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
class RGBLayers(Layers):
        def __init__(self, rgbController):
            Layers.__init__(self)
            self.rgbC = rgbController      

        def activate_layer(self, keyboard, layer, idx=None):
            super().activate_layer(keyboard, layer, idx)
            self.rgbC.on_layer_change(layer)

        def deactivate_layer(self, keyboard, layer):
            super().deactivate_layer(keyboard, layer)
            self.rgbC.on_layer_change(keyboard.active_layers[0])
        
    
rgbLayers = RGBLayers(rgbController )


keyboard.extensions = [
    rgbController
]
keyboard.modules = [
    split, 
    rgbLayers, 
    #keyboard.modules.append(holdtap),
]

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

del Split
del board
del RGB
del Layers
del DiodeOrientation
import gc
gc.collect()

from keyAssignations import assignKeys
keyboard.keymap = assignKeys()

keyboard.debug_enabled = True
#keyboard.powersave_enable()
print("Starting on NML now")
if __name__ == '__main__':
    #keyboard.go(hid_type=HIDModes.BLE )
    keyboard.go( )




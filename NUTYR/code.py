
print("Starting on NRF Right")



def initKB():
    
    from kmk.extensions.media_keys import MediaKeys
    from kmk.modules.mouse_keys import MouseKeys
    from kmk.modules.split import Split, SplitSide,SplitType
    
    from kmk.kmk_keyboard import KMKKeyboard
    from kmk.scanners import DiodeOrientation

    from kmk.scanners.keypad import MatrixScanner
    from kmk.extensions.rgb import RGB
    from kmk.modules.layers import Layers
    import board    
    col_pins = (board.NFC1,board.NFC2,board.D7,board.D8, board.D9,board.D10)
    row_pins = (board.D1,board.D2,board.D3 ,board.D4,)
    
    class RGBController(RGB):
        
        def on_layer_change(self, layer):
            # print("RAULLLLLLLActivating layer", layerArray)
            # layer = layerArray[0]
            if layer == 0:
                self.set_rgb((0, 0, 0), 0)
                self.set_rgb((0, 0, 0), 1)
                self.set_rgb((0, 0, 0), 2)
                self.set_rgb((0, 0, 0), 3)
                self.set_rgb((0, 0, 0), 4)
                self.set_rgb((0, 0, 0), 5)
            elif layer == 1:
                self.set_rgb((0, 0, 0), 0)
                self.set_rgb((self.br, self.br, self.br), 1)
                self.set_rgb((0, 0, 0), 2)
                self.set_rgb((0, 0, 0), 3)
                self.set_rgb((0, 0, 0), 4)
                self.set_rgb((0, 0, 0), 5)
            elif layer == 2:
                self.set_rgb((0, 0, 0), 0)
                self.set_rgb((0, 0, 0), 1)
                self.set_rgb((self.br, self.br, self.br), 2)
                self.set_rgb((0, 0, 0), 3)
                self.set_rgb((0, 0, 0), 4)
                self.set_rgb((0, 0, 0), 5)
            elif layer == 3:
                self.set_rgb((0, 0, 0), 0)
                self.set_rgb((0, 0, 0), 1)
                self.set_rgb((0, 0, 0), 2)
                self.set_rgb((self.br, self.br, self.br), 3)
                self.set_rgb((0, 0, 0), 4)
                self.set_rgb((0, 0, 0), 5)
            self.show()
    
    rgbController = RGBController(
            pixel_pin=board.D0, # GPIO pin of the status LED, or background RGB light
            num_pixels=6,                # one if status LED, more if background RGB light
            rgb_order=(1, 0, 2),
            hue_default=0,               # in range 0-255: 0/255-red, 85-green, 170-blue
            sat_default=0,
            val_default=0,
            )
    

    rgbController.br = 25

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
                max_events=8
            )
    keyboard = MyKeyboard()


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
        data_pin = board.D5,#RX
        data_pin2 = board.D6,#TX
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

    
    from kmk.extensions.media_keys import MediaKeys 
    #from kmk.modules.midi import MidiKeys
    #midiKeys = MidiKeys()
    mouseKeys = MouseKeys()
    mediaKeys = MediaKeys()
    rgbLayers = RGBLayers(rgbController )
    keyboard.extensions = [
        mediaKeys,
        rgbController,
    ]
    keyboard.modules = [
        split, 
        #Layers(), 
        #Power(),
        mouseKeys,
        #midiKeys,
        rgbLayers,
    ]
    
    del Split
    del board
    del RGB
    del Layers
    del DiodeOrientation
    del RGBLayers
    del RGBController
    del MatrixScanner
    del MouseKeys
    del MediaKeys
    #del MidiKeys
    del col_pins
    del row_pins
    import gc
    gc.collect()
    
    from keyAssignations import assignKeys
    keyboard.keymap = assignKeys()
    del assignKeys
    gc.collect()

    return keyboard

if __name__ == '__main__':  
    
    kb = initKB()
    
    kb.debug_enabled = False
    kb.go()

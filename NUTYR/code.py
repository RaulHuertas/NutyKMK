def initKB():
    
    from kmk.extensions.media_keys import MediaKeys
    from kmk.modules.mouse_keys import MouseKeys
    from kmk.modules.spUart import SplitUART, SplitSide
    
    from kmk.kmk_kbUART import KMKKBUART as KMKKeyboard
    from kmk.scanners import DiodeOrientation

    from kmk.scanners.keypad import MatrixScanner
    from kmk.modules.layers import Layers
    import board    
    from time import monotonic
    from math import modf
    from kmk.modules.midi import MidiKeys

    col_pins = (board.NFC1,board.NFC2,board.D7,board.D8, board.D9,board.D10)
    row_pins = (board.D1,board.D2,board.D3 ,board.D4,)



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
                max_events=4
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

    split = SplitUART(
        split_side=SplitSide.RIGHT,
        #split_type=SplitType.UART,
        split_target_left=False,
        data_pin = board.D5,#RX
        data_pin2 = board.D6,#TX
        uart_flip = False,
        debug_enabled = False
    )
    
    class RGBLayers(Layers):
        def __init__(self, pin, brightness=0.2):
            Layers.__init__(self)
            self.br =brightness
            from neopixel import NeoPixel
            self.rgbStrip =  NeoPixel(pin, 6,brightness=self.br)      
            self.wpmC = 0
            self.wpmHigh = False
            
            self.startTime = monotonic()
            
            from digitalio import DigitalInOut, Direction
            self.redLED = DigitalInOut(board.LED_RED)
            self.redLED.direction = Direction.OUTPUT
            self.greenLED = DigitalInOut(board.LED_GREEN)
            self.greenLED.direction = Direction.OUTPUT
            self.blueLED = DigitalInOut(board.LED_BLUE)
            self.blueLED.direction = Direction.OUTPUT
            self.currentLayer = 0

            #initialize lights
            self.on_layer_change(0)
            
        def incrWPM(self, inc=1):
            self.wpmC +=  inc

        def resetWPM(self, inc):
            self.wpmC = 0
            

        def activate_layer(self, keyboard, layer, idx=None):
            super().activate_layer(keyboard, layer, idx)
            self.on_layer_change(layer)

        def deactivate_layer(self, keyboard, layer):
            super().deactivate_layer(keyboard, layer)
            self.on_layer_change(keyboard.active_layers[0])

        def updateLights(self):
            
            nowT = monotonic()
            #blink pulse             
            pulsePosition = (nowT)/1.0 #blink period
            pulseOn = modf(pulsePosition)[0]>0.5 #off cycle
            pulseHighPosition = (nowT)/0.6 #blink period
            pulseHighOn = modf(pulseHighPosition)[0]>0.2 #off cycle
            #wpmHigh
            if((nowT-self.startTime)>1):#update wmpHigh
                self.startTime = nowT
                wpmHighTH = 11##threshold for what high wpm is
                if(self.wpmC>wpmHighTH):
                    self.wpmHigh = True
                else:
                    self.wpmHigh = False
                self.wpmC = 0


            #led status
            GREEN = (0, 255, 0)
            OFF = (0, 0, 0)
            BLUE = (0, 0, 85)
            ORANGE = (234,133,51)
            if pulseOn :
                self.rgbStrip[1] = GREEN
            else:
                self.rgbStrip[1] = OFF
            #led high wpm
            if self.wpmHigh and pulseHighOn :
                self.rgbStrip[0] = ORANGE
            else:
                self.rgbStrip[0] = BLUE


            #####BOARD LEDS
            PURPLE = (180, 0, 255)
            OFF = (0, 0,0)
            #print(layer)
            if self.currentLayer == 0:
                self.rgbStrip[2] = PURPLE
                self.rgbStrip[3] = OFF
                self.rgbStrip[4] = OFF
                self.rgbStrip[5] = OFF
                self.redLED.value = not (True and pulseHighOn)
                self.greenLED.value = not (False and pulseHighOn)
                self.blueLED.value = not (False and pulseHighOn)
            elif self.currentLayer == 1:
                self.rgbStrip[2] = PURPLE
                self.rgbStrip[3] = PURPLE
                self.rgbStrip[4] = OFF
                self.rgbStrip[5] = OFF
                self.redLED.value = not (False and pulseHighOn)
                self.greenLED.value = not (True and pulseHighOn)
                self.blueLED.value = not (False and pulseHighOn)
            elif self.currentLayer == 2:
                self.rgbStrip[2] = PURPLE
                self.rgbStrip[3] = PURPLE
                self.rgbStrip[4] = PURPLE
                self.rgbStrip[5] = OFF
                self.redLED.value = not (False and pulseHighOn)
                self.greenLED.value = not (False and pulseHighOn)
                self.blueLED.value = not (True and pulseHighOn)
            elif self.currentLayer == 3:
                self.rgbStrip[2] = PURPLE
                self.rgbStrip[3] = PURPLE
                self.rgbStrip[4] = PURPLE
                self.rgbStrip[5] = PURPLE
                self.redLED.value = not (True and pulseHighOn)
                self.greenLED.value = not (True and pulseHighOn)
                self.blueLED.value = not (True and pulseHighOn)

        def before_matrix_scan(self, sandbox):
            super().before_matrix_scan(sandbox)
            self.updateLights()

        def after_matrix_scan(self, keyboard):
            super().after_matrix_scan(keyboard)
            

        def before_hid_send(self, keyboard):
            super().before_hid_send(keyboard)
            if keyboard.hid_pending:
                self.incrWPM(1)     
        def after_hid_send(self, keyboard):
            super().after_hid_send(keyboard)

        def on_layer_change(self, layer):
            nowT = monotonic()
            self.currentLayer = layer
            self.updateLights()
            
            


           
    
    from kmk.extensions.media_keys import MediaKeys 
    mouseKeys = MouseKeys()
    mediaKeys = MediaKeys()
    rgbLayers = RGBLayers(board.D0, 0.05 )
    midi = MidiKeys()
    #keyboard.modules.append()

    keyboard.extensions = [
        mediaKeys,
        #locks
    ]
    keyboard.modules = [
        split, 
        #Layers(), 
        #Power(),
        mouseKeys,
        #midiKeys,
        rgbLayers,
        midi,
    ]
    
    del SplitUART
    #del Split
    del board
    del Layers
    del DiodeOrientation
    del RGBLayers
    del MatrixScanner
    del MouseKeys
    del MediaKeys
    del midi
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

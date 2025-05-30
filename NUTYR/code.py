GREEN = (0, 255, 0)
OFF = (0, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (234,133,51)
RED = (255, 0, 0)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (128, 128, 0)
BLACK = (0, 0, 0)
import time

testing  = False

def isItOn(cols, rows, keyIndex):
    nCol = len(cols)
    nRow = len(rows)
    colPins = [None]*nCol 
    rowPins = [None]*nRow 
    import digitalio
    for i in range(nCol):
        colPin = colPins[i] = digitalio.DigitalInOut(cols[i])
        colPin.direction = digitalio.Direction.OUTPUT
        colPin.value = False
    for i in range(nRow):
        rowPin = rowPins[i] = digitalio.DigitalInOut(rows[i])
        rowPin.direction = digitalio.Direction.INPUT
        rowPin.pull = digitalio.Pull.UP

    colIndex = keyIndex % nCol
    rowIndex = keyIndex // nCol
    #Setup the columns. The one active must be low, the rest high
    for c in range(nCol):
        if c == colIndex:
            colPins[c].value = False
        else:
            colPins[c].value = True
    #Final read of the switch
    import time
    time.sleep(0.01)
    returnVal = rowPins[rowIndex].value

    for i in range(nRow):
        rowPins[i].direction = digitalio.Direction.INPUT
        rowPins[i].deinit()
    

    for i in range(nCol):
        colPins[i].direction = digitalio.Direction.INPUT
        colPins[i].deinit()

    return not returnVal

def restartBLE():
    import _bleio
    _bleio.adapter.erase_bonding()

bleSelectButton = 18
import board
col_pins = (board.NFC1,board.NFC2,board.D7,board.D8, board.D9,board.D10)
row_pins = (board.D1,board.D2,board.D3 ,board.D4,)

bleEnabled = isItOn(col_pins, row_pins, bleSelectButton)
print("BLE enabled: ",bleEnabled)
if bleEnabled:
    if isItOn(col_pins, row_pins, 5) and isItOn(col_pins, row_pins, 5):
        import _bleio
        _bleio.adapter.erase_bonding()
        print("Erased bonding")

del isItOn
del board
del col_pins
del row_pins

def initKB():
    global bleEnabled
    from kmk.scanners import DiodeOrientation

    from kmk.scanners.keypad import MatrixScanner
    from kmk.modules.layers import Layers
    from time import monotonic
    from math import modf
    from kmk.keys import ConsumerKey, make_key

    import board
    import pwmio
    col_pins = (board.NFC1,board.NFC2,board.D7,board.D8, board.D9,board.D10)
    row_pins = (board.D1,board.D2,board.D3 ,board.D4,)
    diode_orientation = DiodeOrientation.ROW2COL

    if not bleEnabled:
        from kmk.usbkb import  USBKB
        class MyKeyboard(USBKB):
            def __init__(self, col_pins, row_pins):   
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
        keyboard = MyKeyboard(col_pins, row_pins)
    else:
        from nkble import NKB_BLE
        from kmk.scanners import DiodeOrientation
        diode_orientation = DiodeOrientation.ROW2COL
        keyboard = NKB_BLE(
            row_pins=row_pins,  
            col_pins=col_pins,
            diode_orientation=diode_orientation,
        )

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

    if bleEnabled:
        from kmk.modules.splitbl import SplitBL, SplitSide, SplitRole
        split = SplitBL(
            split_side=SplitSide.RIGHT,
            split_role=SplitRole.Primary,
            debug_enabled = testing 
        )
    else:
        from kmk.modules.splituart import SplitUART, SplitSide
        split = SplitUART(
            split_side=SplitSide.RIGHT,
            split_target_left=False,
            data_pin = board.D5,#RX
            data_pin2 = board.D6,#TX
            debug_enabled = testing
        )
    
    class RGBLayers(Layers):
        def __init__(self, pin, nLeds=6,brightness=0.2):
            Layers.__init__(self)
            self.br =brightness
            if not bleEnabled:
                from neopixel import NeoPixel
                self.rgbStrip =  NeoPixel(pin, 6,brightness=self.br , auto_write=False)      
            self.wpmC = 0
            self.wpmHigh = False
            self.nLeds = nLeds
            self.simpleLights = nLeds<=6 
            
            self.startTime = monotonic()
            
            self.ledAnimTime = monotonic()
            from digitalio import DigitalInOut, Direction
            self.redLED = pwmio.PWMOut(board.LED_RED, frequency=5000, duty_cycle=0)
            self.greenLED = pwmio.PWMOut(board.LED_GREEN, frequency=5000, duty_cycle=0)
            self.blueLED = pwmio.PWMOut(board.LED_BLUE, frequency=5000, duty_cycle=0)

            self.currentLayer = 0

            self.updateLights(  )
            
            #initialize media
            mediaCodes = (
                (0xE2, ('AUDIO_MUTE', 'MUTE')),
                (0xE9, ('AUDIO_VOL_UP', 'VOLU')),
                (0xEA, ('AUDIO_VOL_DOWN', 'VOLD')),
                (0x6F, ('BRIGHTNESS_UP', 'BRIU')),
                (0x70, ('BRIGHTNESS_DOWN', 'BRID')),
                (0xB5, ('MEDIA_NEXT_TRACK', 'MNXT')),
                (0xB6, ('MEDIA_PREV_TRACK', 'MPRV')),
                (0xB7, ('MEDIA_STOP', 'MSTP')),
                (0xCD, ('MEDIA_PLAY_PAUSE', 'MPLY')),
                #(0xB8, ('MEDIA_EJECT', 'EJCT')),
                (0xB3, ('MEDIA_FAST_FORWARD', 'MFFD')),
                (0xB4, ('MEDIA_REWIND', 'MRWD')),
            )

            for code, names in mediaCodes:
                make_key(names=names, constructor=ConsumerKey, code=code)

        def incrWPM(self, inc=1):
            self.wpmC +=  inc

        def resetWPM(self):
            self.wpmC = 0
            

        def activate_layer(self, keyboard, layer, idx=None):
            super().activate_layer(keyboard, layer, idx)
            self.on_layer_change(layer)

        def deactivate_layer(self, keyboard, layer):
            super().deactivate_layer(keyboard, layer)
            self.on_layer_change(keyboard.active_layers[0])
            
        def stripAnim(self):
            if bleEnabled:
                return
            MAINCOLOR = RED
            for pix in range(self.nLeds):
                if pix<=self.currentLayer:                
                    self.rgbStrip[pix] = MAINCOLOR if (not self.wpmHigh) else ( BLACK if self.pulseOn else MAINCOLOR)
                else:
                    self.rgbStrip[pix] = BLACK

        def updateLights(self):
            nowT = monotonic()
            if ((nowT-self.ledAnimTime)<0.050):
                return
            #blink pulse             
            pulsePosition = (nowT)/2.0 #blink period
            self.pulseOn = modf(pulsePosition)[0]>0.9 #off cycle
            pulseHighPosition = (nowT)/0.350 #blink period
            self.pulseHighOn = modf(pulseHighPosition)[0]>0.5 #off cycle
            #wpmHigh
            if((nowT-self.startTime)>1):#update wmpHigh
                self.startTime = nowT
                wpmHighTH = 11##threshold for what high wpm is
                if(self.wpmC>wpmHighTH):
                    self.wpmHigh = True
                else:
                    self.wpmHigh = False
                self.resetWPM()

            #######################
            ######LEDS status######
            #######################

            
            dtcyc = 60000
            dtcycOff = 65535
            #onLedValue = dtcyc #if self.pulseHighOn else 65535
            onLedValue= dtcyc if self.pulseHighOn else 65535
            if self.currentLayer == 0:
                self.redLED.duty_cycle = onLedValue
                self.greenLED.duty_cycle = dtcycOff
                self.blueLED.duty_cycle = dtcycOff
            elif self.currentLayer == 1:
                self.redLED.duty_cycle = dtcycOff
                self.greenLED.duty_cycle = onLedValue
                self.blueLED.duty_cycle = dtcycOff
            elif self.currentLayer == 2:
                self.redLED.duty_cycle = dtcycOff
                self.greenLED.duty_cycle = dtcycOff
                self.blueLED.duty_cycle = onLedValue
            elif self.currentLayer == 3:
                self.redLED.duty_cycle = onLedValue
                self.greenLED.duty_cycle = onLedValue
                self.blueLED.duty_cycle = dtcycOff
            elif self.currentLayer == 4:
                self.redLED.duty_cycle = onLedValue
                self.greenLED.duty_cycle = dtcycOff
                self.blueLED.duty_cycle = onLedValue
            
            if not bleEnabled:
                self.stripAnim()
                self.rgbStrip.show()
            
            self.ledAnimTime = nowT

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
    
    lightsFeedback = RGBLayers(pin=board.D0, nLeds=6, brightness=0.03)

    if bleEnabled:
        from kmk.modules.power import Power
        power = Power()
        from kmk.modules.mouse_keys import MouseKeys
        keyboard.modules = [
            split, 
            MouseKeys(),
            lightsFeedback,
            power
        ]
    else:
        from kmk.modules.midi import MidiKeys
        from kmk.modules.mouse_keys import MouseKeys
        keyboard.modules = [
            split, 
            MouseKeys(),
            lightsFeedback,
            MidiKeys()
        ]
    
    #del Split
    del board
    del Layers
    del DiodeOrientation
    del RGBLayers
    del MatrixScanner
    #del MouseKeys
    #del MediaKeys
    del col_pins
    del row_pins
    import gc
    gc.collect()
    print('mem_info used:', gc.mem_alloc(), ' free:', gc.mem_free())
    from keyAssignations import assignKeys
    keyboard.keymap = assignKeys()
    del assignKeys
    gc.collect()

    return keyboard

if __name__ == '__main__':  
    
    kb = initKB()
    
    kb.debug_enabled = testing
    
    if bleEnabled:
        kb.powersave_enable = True
        kb.go()
    else:
        kb.go()


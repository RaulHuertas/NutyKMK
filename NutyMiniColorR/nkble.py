
from kmk.scanners.keypad import MatrixScanner
from kmk.modules.layers import Layers
from time import monotonic
from math import modf
from kmk.kbble import KMKBLEKeyboard
from kmk.keys import ConsumerKey, make_key
from kmk.keys import KeyboardKey, make_key
from microcontroller import nvm

import pwmio
import board

class NKB_BLE(KMKBLEKeyboard):
    def __init__(self, col_pins, row_pins, diode_orientation):   
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
        import digitalio
        self.chargeFastPin = digitalio.DigitalInOut(board.CHARGE_RATE)
        self.chargeFastPin.direction = digitalio.Direction.OUTPUT
        self.chargeFastPin.value = False

    
 
class BLEFeedback(Layers):

    def __init__(self):
        Layers.__init__(self)
        
        from kmk.keys import make_key,Key


        self.wpmC = 0
        self.wpmHigh = False
        
        self.startTime = monotonic()
        
        self.ledAnimTime = monotonic()
        from digitalio import DigitalInOut, Direction
        self.redLED = pwmio.PWMOut(board.LED_RED, frequency=5000, duty_cycle=0)
        self.greenLED = pwmio.PWMOut(board.LED_GREEN, frequency=5000, duty_cycle=0)
        self.blueLED = pwmio.PWMOut(board.LED_BLUE, frequency=5000, duty_cycle=0)

        
        self.currentLayer = 0

        #initialize lights
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

        # International
        codes = (
            (50, ('NONUS_HASH', 'NUHS')),
            (100, ('NONUS_BSLASH', 'NUBS')),
            (101, ('APP', 'APPLICATION', 'SEL', 'WINMENU')),
            (135, ('INT1', 'RO')),
            (136, ('INT2', 'KANA')),
            (137, ('INT3', 'JYEN')),
            (138, ('INT4', 'HENK')),
            (139, ('INT5', 'MHEN')),
            (140, ('INT6',)),
            (141, ('INT7',)),
            (142, ('INT8',)),
            (143, ('INT9',)),
            (144, ('LANG1', 'HAEN')),
            (145, ('LANG2', 'HAEJ')),
            (146, ('LANG3',)),
            (147, ('LANG4',)),
            (148, ('LANG5',)),
            (149, ('LANG6',)),
            (150, ('LANG7',)),
            (151, ('LANG8',)),
            (152, ('LANG9',)),
        )
        for code, names in codes:
            make_key(names=names, constructor=KeyboardKey, code=code)

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
  
    def updateLights(self):
        
        nowT = monotonic()
        if ((nowT-self.ledAnimTime)<0.050):
            return
        #blink pulse             
        pulsePosition = (nowT)/2.0 #blink period
        pulseOn = modf(pulsePosition)[0]>0.9 #off cycle
        pulseHighPosition = (nowT)/0.35 #blink period
        pulseHighOn = modf(pulseHighPosition)[0]>0.9 #off cycle
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
        

            
        
        dtcyc = 50000
        dtcycOff = 65535
        onLedValue= dtcyc if pulseHighOn else 65535
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



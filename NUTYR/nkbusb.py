from kmk.usbkb import  USBKB

from kmk.scanners.keypad import MatrixScanner
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers

from time import monotonic, sleep
from math import modf
from kmk.keys import ConsumerKey, make_key
from kmk.keys import KeyboardKey, make_key
from microcontroller import nvm

import pwmio
import board
GREEN = (0, 255, 0)
OFF = (0, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (234,133,51)
RED = (255, 0, 0)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (128, 128, 0)
BLACK = (0, 0, 0)
PRIMARYCOLOR = (201,20, 20)

def paintRandom(strip, nLeds):
    import random
    for pixel in range(nLeds):
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        strip[pixel] = (r,g,b)

def rgbClamp(value):
    if value > 255:
        return 255
    if value < 0:
        return 0
    return value

def lightShow(strip, nPixels, stageTime=0.15, nStages =10):
    import random
    for stage in range(nStages):
        paintRandom(strip,nPixels)
        strip.show()
        sleep(stageTime)
    
class NKB_USB(USBKB):
    def __init__(self, col_pins, row_pins, diode_orientation = DiodeOrientation.ROW2COL):   
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
        import digitalio
        chargeFastPin = digitalio.DigitalInOut(board.CHARGE_RATE)
        chargeFastPin.direction = digitalio.Direction.OUTPUT
        chargeFastPin.value = False

class USBFeedback(Layers):
    brightnessStep : int#0 to 5
    speed : int
    
    def restoreNVM(self):
        self.brightnessStep = nvm[0]
        self.effect = nvm[1]
        self.speed = nvm[2]
        #print("self.brightnessStep:",self.brightnessStep)
        #print("self.effect:",self.effect)

    def saveNVM(self):
        #print("start save")
        #print(dir(self.nvm))
        toStore = self.brightnessStep.to_bytes(1,'little')+self.effect.to_bytes(1,'little')+self.speed.to_bytes(1,'little')
        nvm[0:3] =    toStore     #self.nvm.__setitem__(0,self.brightnessStep)
        #self.nvm.__setitem__(1,self.effect)
        #print("end save")

        #self.nvm[0] = self.brightnessStep
        #self.nvm[1] = self.effect   

    def _applyBrightness(self):
       self.rgbStrip.brightness = 0.5*self.brightnessStep/4.0 
       self.rgbStrip.show()

    def _applyEffect(self):
        if self.effect == 0:
            self.fullyPaintAs(PRIMARYCOLOR)
        elif self.effect == 1:
            self.startRandomEffect()
        elif self.effect == 2:
            self.fullyPaintAs(BLUE)
        else:
            self.fullyPaintAs(WHITE)
        
        pass

    def restartLights( self, *args, **kwargs):
        self.brightnessStep = 3
        self.effect = 0
        self.speed = 30
        self.saveNVM()
        self._applyBrightness()
        self._applyEffect()

    def changeBrightness( self, *args, **kwargs):
        self.brightnessStep += 1
        self.brightnessStep%=5
        self._applyBrightness()
        self.saveNVM()
    
    def changeEffect( self, *args, **kwargs):
        self.effect += 1
        self.effect%=4
        self._applyEffect()
        self.saveNVM()
        
    def reduceLightsSpeed( self, *args, **kwargs):
        self.speed -= 10
        if self.speed<0:
            self.speed = 0
        self.startRandomDirectionValues()
        self.saveNVM()
    
    def increaseLightsSpeed( self, *args, **kwargs):
        self.speed += 10
        if self.speed>100:
            self.speed = 100
        self.startRandomDirectionValues()
        self.saveNVM()
    
    def restoreLights(self):
        #self.fullyPaintAs(PINK)
        self._applyEffect()
        self.rgbStrip.show()
        
    
    def __init__(self, pin, nLeds = 128, brightness=0.2):
        import random
        
        
        Layers.__init__(self)
        self.restoreNVM() 
        
        
        self.randomLightsBuffer = [(0,0,0)]*21
        self.startRandomEffectValues()
        self.randomLightsDirection = [(1,-1,1)]*21
        self.startRandomDirectionValues()
        
        
        from kmk.keys import make_key,Key
        make_key(names=('BRIGHT_STEP',),constructor=Key, on_press=self.changeBrightness)
        make_key(names=('EFFECT_STEP',),constructor=Key, on_press=self.changeEffect)
        make_key(names=('LIGHTS_LESS_SPEED',),constructor=Key, on_press=self.reduceLightsSpeed)    
        make_key(names=('LIGHTS_MORE_SPEED',),constructor=Key, on_press=self.increaseLightsSpeed)        
        make_key(names=('LIGHTS_RESET',),constructor=Key, on_press=self.restartLights)
        

        self.br =brightness
        from neopixel import NeoPixel
        self.rgbStrip =  NeoPixel(pin, nLeds,brightness=self.br , auto_write=False)     
        self.nLeds = nLeds
        self.simpleLights = nLeds<=6
        lightShow(self.rgbStrip, nLeds)
        for pix in range(nLeds):
            self.rgbStrip[pix] = (0,255,0) 
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

    def fullyPaintAs(self, color):
        for pix in range(self.nLeds):
            self.rgbStrip[pix] = color 
        

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
  
    def assignColorToLayerIndicator(self, color):
        if self.simpleLights:
            return
        self.rgbStrip[21] = color
        self.rgbStrip[22] = color
        self.rgbStrip[23] = color

    def stripAnim(self):
        MAINCOLOR = RED
        if self.simpleLights:
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
        pulseOn = modf(pulsePosition)[0]>0.9 #off cycle
        pulseHighPosition = (nowT)/0.4 #blink period
        pulseHighOn = modf(pulseHighPosition)[0]>0.5 #off cycle
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
        
        def pulsed(color, pulseColor, pulseOn,usePulse):
            if usePulse:
                if pulseOn:
                    return pulseColor
                else:
                    return OFF
            else:
                return color
            
        
        dtcyc = 30000
        dtcycOff = 65535

        if self.currentLayer == 0:
            self.assignColorToLayerIndicator( pulsed(RED,PURPLE, pulseHighOn, self.wpmHigh))
            self.redLED.duty_cycle = dtcyc
            self.greenLED.duty_cycle = dtcycOff
            self.blueLED.duty_cycle = dtcycOff
        elif self.currentLayer == 1:
            self.assignColorToLayerIndicator( pulsed(GREEN,PURPLE, pulseHighOn, self.wpmHigh))
            self.redLED.duty_cycle = dtcycOff
            self.greenLED.duty_cycle = dtcyc
            self.blueLED.duty_cycle = dtcycOff
        elif self.currentLayer == 2:
            self.assignColorToLayerIndicator( pulsed(BLUE,PURPLE, pulseHighOn, self.wpmHigh)) 
            self.redLED.duty_cycle = dtcycOff
            self.greenLED.duty_cycle = dtcycOff
            self.blueLED.duty_cycle = dtcyc
        elif self.currentLayer == 3:
            self.assignColorToLayerIndicator( pulsed(YELLOW,PURPLE, pulseHighOn, self.wpmHigh))
            self.redLED.duty_cycle = dtcyc
            self.greenLED.duty_cycle = dtcyc
            self.blueLED.duty_cycle = dtcycOff
        elif self.currentLayer == 4:
            self.assignColorToLayerIndicator( pulsed(WHITE,PURPLE, pulseHighOn, self.wpmHigh))
            self.redLED.duty_cycle = dtcyc
            self.greenLED.duty_cycle = dtcycOff
            self.blueLED.duty_cycle = dtcyc

        self.stripAnim()        
        #animate random effect
        if (self.effect == 1) and (not self.simpleLights):
            for p in range(21):
                pixel = self.randomLightsBuffer[p]
                stepRed = self.randomLightsDirection[p][0]
                stepGreen = self.randomLightsDirection[p][1]
                stepBlue = self.randomLightsDirection[p][2]
                newRed      = rgbClamp((pixel[0]+stepRed))
                if(newRed>=255 or newRed<=0):
                    stepRed = -stepRed
                newGreen    = rgbClamp((pixel[1]+stepGreen))
                if(newGreen>=255 or newGreen<=0):
                    stepGreen = -stepGreen
                newBlue     = rgbClamp((pixel[2]+stepBlue))
                if(newBlue>=255 or newBlue<=0):
                    stepBlue = -stepBlue
                
                self.randomLightsBuffer[p] = (newRed,newGreen,newBlue)
                self.randomLightsDirection[p] = (stepRed,stepGreen,stepBlue)

            self.randomEffectBufferToLights() 
        
        self.rgbStrip.show()
        self.ledAnimTime = nowT

    def randomEffectBufferToLights(self):

        for i in range(21):
            self.rgbStrip[i] = self.randomLightsBuffer[i]
            
    def startRandomDirectionValues(self):
        import random
        speed = self.speed
        
        print("Assign random colors!!")
        for pixel in range(21):
            r = -1 if random.randint(0,1)==0 else 1
            g = -1 if random.randint(0,1)==0 else 1
            b = -1 if random.randint(0,1)==0 else 1
            self.randomLightsDirection[pixel] = (r*speed,g*speed,b*speed)

    def startRandomEffectValues(self):
        import random
        
        print("Assign random colors!!")
        for pixel in range(21):
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            self.randomLightsBuffer[pixel] = (r,g,b)
            
    def startRandomEffect(self):
        self.startRandomEffectValues()
        self.randomEffectBufferToLights()

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
        
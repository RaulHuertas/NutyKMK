import gc
# add other imports

gc.collect()
start_mem = gc.mem_free()
print( "Point 1 Available memory: {} bytes".format(start_mem) ) 



print("Starting on Mini Macro Keyboard")
# Import all board pins.
#import board
#import busio
#
## Import the SSD1306 module.
#import adafruit_ssd1306
#
#
## Create the I2C interface.
#i2c = busio.I2C(board.D0, board.D1)
#
#
#display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
#display.fill(0)
#
## Set a pixel in the origin 0,0 position.
#display.pixel(0, 0, 1)
## Set a pixel in the middle 64, 16 position.
#display.pixel(64, 16, 1)
## Set a pixel in the opposite 127, 31 position.
#display.pixel(127, 31, 1)
#display.text("Hello, World!", 0, 0, 1)
#
#
#display.show()
#
import board


col_pins = (board.D7,board.D8, board.D9)
row_pins = (board.NFC1,board.NFC2)


dirPins = [
    board.D2,  board.D3,  board.D4, board.D5, board.D6,
]

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
        rowPins[i].deinit()
    

    for i in range(nCol):
        colPins[i].deinit()

    return not returnVal
buttonToTestIndex = 5
print("Button "+str(buttonToTestIndex)+" is pressed: ", isItOn(col_pins, row_pins, buttonToTestIndex))
        

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.scanners.keypad import KeysScanner
from kmk.scanners.keypad import MatrixScanner
from kmk.keys import KC
from kmk.hid import HIDModes

from keyAssignations import assignKeys

diode_orientation = DiodeOrientation.ROW2COL

class MyKeyboard(KMKKeyboard):
    def __init__(self):
        # create and register the scanner
        self.matrix = [ 
            MatrixScanner(
            # required arguments:
            column_pins=col_pins,
            row_pins=row_pins,
            # optional arguments with defaults:
            columns_to_anodes=diode_orientation,
            interval=0.020,  # Debounce time in floating point seconds
            max_events=64
        ),
        KeysScanner(
            # require argument:
            pins=dirPins,
            # optional arguments with defaults:
            value_when_pressed=False,
            pull=True,
            interval=0.02,  # Debounce time in floating point seconds
            max_events=8
        ),
        ]
keyboard = MyKeyboard()
keyboard.debug_enabled = False


keyboard.coord_mapping =  [
    0,  1,  2,  3,  4,  5, 6, 7,  8,9,10
]




layer0Asignations = [ KC.NO]*11
layer0Asignations[0] =  KC.I
layer0Asignations[1] =  KC.J
layer0Asignations[2] =  KC.K
layer0Asignations[3] =  KC.L
layer0Asignations[4] =  KC.M
layer0Asignations[5] =  KC.N

layer0Asignations[6] =  KC.ENTER
layer0Asignations[7] =  KC.UP
layer0Asignations[8] =  KC.RIGHT
layer0Asignations[9] =  KC.DOWN
layer0Asignations[10] =  KC.LEFT

keyboard.keymap = [
    layer0Asignations
]

#power = Power()
#keyboard.modules.append(power)
#keyboard.powersave_enable = True
keyboard.debug_enabled = True
print("starting loop")
if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.BLE, ble_name="NutyPico")
    #keyboard.go()



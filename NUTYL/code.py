
print("Starting on NML")

testing = True

def isItOn(cols, rows, keyIndex):
    import time
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
import board
bleSelectButton = 23
col_pins = (board.D1,board.D2,board.D3,board.D4, board.D5,board.D6,)
row_pins = (board.NFC1, board.NFC2, board.D7,board.D8,)
bleEnabled  = isItOn(col_pins, row_pins, bleSelectButton)
del board
del isItOn

def initKB():
    import board
    col_pins = (board.D1,board.D2,board.D3,board.D4, board.D5,board.D6,)
    row_pins = (board.NFC1, board.NFC2, board.D7,board.D8,)
    global bleEnabled 
    global testing
    print("BLE enabled: ",bleEnabled)
    if bleEnabled:
        from nkbble import NKB_BLE           
        keyboard = NKB_BLE(col_pins, row_pins)
        from kmk.extensions.display import Display
        from kmk.extensions.display.ssd1306 import SSD1306
        import busio
        i2c_bus = busio.I2C(board.D9, board.D10)
        driver = SSD1306(
            i2c=i2c_bus,
            width=32,
            height=128,
            rotation=270
        )
        display = Display(
            display=driver,
            brightness=0.4, # initial screen brightness level
            brightness_step=0.1, # used for brightness increase/decrease keycodes
            dim_time=0.5, # time in seconds to reduce screen brightness
            dim_target=0.05, # set level for brightness decrease
            off_time=5, # time in seconds to turn off screen
            powersave_dim_time=10, # time in seconds to reduce screen brightness
            powersave_dim_target=0.1, # set level for brightness decrease
            powersave_off_time=12, # time in seconds to turn off screen
        )

        keyboard.extensions.append(display)
        from kmk.modules.layers import Layers
        keyboard.modules.append([
            Layers()
        ])

    else:
        from kmk.kbusb import KMKKeyboard
        class MyKeyboard(KMKKeyboard):
            def __init__(self, col_pins, row_pins):   
                # create and register the scanner
                self.matrix = MatrixScanner(
                    # required arguments:
                    column_pins=col_pins,
                    row_pins=row_pins,
                    # optional arguments with defaults:
                    interval=0.020,  # Debounce time in floating point seconds
                    max_events=4
                )               
        keyboard = MyKeyboard(col_pins, row_pins)
        
    del board
    del col_pins
    del row_pins

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

    split = None
    if bleEnabled:
        from kmk.modules.splitbl import SplitBL, SplitSide, SplitRole
        split = SplitBL(
            split_side=SplitSide.LEFT,
            split_role=SplitRole.Secondary,
            debug_enabled = testing 
        )
    else:
        from kmk.modules.splituart import SplitUART, SplitSide
        split = SplitUART(
            split_side=SplitSide.LEFT,
            #split_side=None,
            split_target_left=True,
            data_pin = board.D9,#RX
            data_pin2 = board.IMU_PWR,#TX
            debug_enabled = testing
        )
    

    if bleEnabled:
        #from kmk.modules.mouse_keys import MouseKeys 
        #mouseKeys = MouseKeys()
        #from nkbble import BLEFeedback
        #lightsFeedBack = BLEFeedback(board.D0, 0.03 )
        from kmk.modules.power import Power
        power = Power()
        keyboard.modules = [
            split, 
            #mouseKeys,
            #lightsFeedBack, 
            power
        ]
        from keyAssignationsBLE import assignKeys
        keyboard.keymap = assignKeys()
    else:
        from kmk.modules.mouse_keys import MouseKeys         
        from kmk.modules.midi import MidiKeys
        from nkbusb import USBFeedback
        lightsFeedBack = USBFeedback(board.D0, 0.03 )
        keyboard.modules = [
            split, 
            MouseKeys(),
            lightsFeedBack, 
            MidiKeys()
        ]
        
        from keyAssignations import assignKeys
        keyboard.keymap = assignKeys()

        

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

    
    import gc
    gc.collect()
   
    return keyboard


if __name__ == '__main__':
    print("Starting on NML now")
    kb = initKB()
    kb.debug_enabled = testing

    if bleEnabled:
        kb.powersave_enable = True
        kb.go(False)
    else:
        kb.go( )




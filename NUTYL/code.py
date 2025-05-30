
print("Starting on NML")

testing = False

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
        import os
        
        oled = os.getenv("NLOLED")!=0
        if oled:
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
            #driver.root_group = None
            display = Display(
                display=driver,
                brightness=0.4, # initial screen brightness level
                brightness_step=0.1, # used for brightness increase/decrease keycodes
                dim_time=5.0, # time in seconds to reduce screen brightness
                dim_target=0.03, # set level for brightness decrease
                off_time=15, # time in seconds to turn off screen
                powersave_dim_time=10, # time in seconds to reduce screen brightness
                powersave_dim_target=0.1, # set level for brightness decrease
                powersave_off_time=12, # time in seconds to turn off screen
            )
            from kmk.modules.layers import Layers
            keyboard.extensions.append(display)
            keyboard.modules.append(Layers())
        else:
            from nkbble import BLEFeedback
            lightsFeedBack = BLEFeedback( )
            keyboard.modules.append(lightsFeedBack) 
        

    else:
        from nkbusb import NKB_USB
        keyboard = NKB_USB(col_pins=col_pins, row_pins=row_pins)

        
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
        import board
        split = SplitUART(
            split_side=SplitSide.LEFT,
            split_target_left=False,
            data_pin = board.D9,#RX
            data_pin2 = board.D10,#TX
            debug_enabled = testing
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
        #from kmk.modules.mouse_keys import MouseKeys 
        #mouseKeys = MouseKeys()
        #from nkbble import BLEFeedback
        #lightsFeedBack = BLEFeedback(board.D0, 0.03 )
        from kmk.modules.power import Power
        power = Power()
        keyboard.modules.append(split)
        keyboard.modules.append(power)
        from keyAssignationsBLE import assignKeys
        keyboard.keymap = assignKeys()
    else:
        from nkbusb import USBFeedback
        lightsFeedBack = USBFeedback(board.D0,nLeds=6,brightness= 0.03 )
        keyboard.modules = [
            split, 
            lightsFeedBack, 
        ]
        
        from keyAssignations import assignKeys
        keyboard.keymap = assignKeys()

        


    
    import gc
    gc.collect()
   
    return keyboard


if __name__ == '__main__':
    print("Starting on NML now")
    kb = initKB()
    kb.debug_enabled = testing

    if bleEnabled:
        kb.powersave_enable = True
        kb.go(isTarget=False)
    else:
        kb.go( )




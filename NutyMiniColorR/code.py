print("Starting on RIGHT")

import board
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

row_pins = (board.D4, board.D3, board.D2, board.D1)
col_pins = ( board.D5, board.D6,board.D7, board.D8,board.D9,board.D10,)
bleSelectButton = 18
testing = False

def initKBUSB():
    from nkbusb import NKB_USB, USBFeedback
    from kmk.modules.splituart import SplitUART, SplitSide
            
    split = SplitUART(
        split_side=SplitSide.RIGHT,
        split_target_left=False,
        data_pin = board.NFC2,#RX
        data_pin2 = board.NFC1,#TX
        debug_enabled = testing
    )

    keyboard = NKB_USB(col_pins, row_pins)

    
    fb = USBFeedback(board.D0, 24, 0.1)
    
    from kmk.modules.holdtap import HoldTap
    
    from kmk.modules.mouse_keys  import MouseKeys
    holdtap = HoldTap()
    keyboard.modules = [
        split, 
        fb,
        holdtap,
        MouseKeys()
    ]

    return keyboard

def initKBBLE():
    from nkble import BLEFeedback
    from kmk.scanners import DiodeOrientation
    from nkble import NKB_BLE
    global row_pins, col_pins
    diode_orientation = DiodeOrientation.ROW2COL
    keyboard = NKB_BLE(col_pins, row_pins,diode_orientation)
    from kmk.modules.splitbl import SplitBL, SplitSide, SplitRole
    split = SplitBL(
        split_side=SplitSide.RIGHT,
        split_role=SplitRole.Primary,
        debug_enabled = testing
    )
    from kmk.modules.power import Power
    power = Power()
    from kmk.modules.holdtap import HoldTap
    from kmk.modules.mouse_keys import MouseKeys
    
    keyboard.modules = [
        split,
        power,
        HoldTap(),
        MouseKeys(),
        BLEFeedback()
    ]         
    
    return keyboard            

def assignKeymap(kb):
    from keyAssignations import assignKeys
    kb.keymap = assignKeys()
bleEnabled = isItOn(col_pins, row_pins, bleSelectButton)
print("BLE ENABLED: ", bleEnabled)

if __name__ == '__main__':
    keyboard = None
    if bleEnabled:    
        keyboard = initKBBLE()
    else:
        keyboard = initKBUSB()
    
    
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
    
    assignKeymap(keyboard)

    keyboard.debug_enabled = testing
    keyboard.go()





print("Starting on LEFT")

import board
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
row_pins = (board.D7, board.D8, board.D9, board.D10,)
col_pins = ( board.D1, board.D2,board.D3, board.D4,board.D5,board.D6)
bleSelectButton = 23

def initKBUSB():
    from nkbusb import NKB_USB, USBFeedback
    from kmk.modules.splituart import SplitUART, SplitSide

    keyboard = NKB_USB(col_pins, row_pins)
    split = SplitUART(
            split_side=SplitSide.LEFT,
            split_target_left=True,
            data_pin = board.NFC1,#RX
            data_pin2 = board.NFC2,#TX
            debug_enabled = testing
        )
    from kmk.modules.holdtap import HoldTap
    from kmk.modules.mouse_keys import MouseKeys
    from kmk.modules.layers import Layers
    keyboard.modules = [
        split, 
        USBFeedback(board.D0, 24,brightness=0.1),
        HoldTap(),
        MouseKeys(),
        Layers()
    ]

    
    return keyboard


def initKBBLE():
    
    from kmk.kbble import KMKBLEKeyboard
    from kmk.scanners.keypad import MatrixScanner
    from kmk.scanners import DiodeOrientation
    class MyKeyboard(KMKBLEKeyboard):
        def __init__(self, col_pins, row_pins):   
            # create and register the scanner
            self.matrix = MatrixScanner(
                # required arguments:
                column_pins=col_pins,
                row_pins=row_pins,
                # optional arguments with defaults:
                columns_to_anodes=DiodeOrientation.COL2ROW,
                interval=0.020,  # Debounce time in floating point seconds
                max_events=4
            )
    
    keyboard = MyKeyboard(col_pins, row_pins)

    from kmk.modules.splituart import SplitUART, SplitSide
    split = SplitUART(
            split_side=SplitSide.LEFT,
            split_target_left=True,
            data_pin = board.NFC1,#RX
            data_pin2 = board.NFC2,#TX
            debug_enabled = testing
        )   
    from kmk.modules.power import Power
    power = Power()
    from kmk.modules.holdtap import HoldTap
    from kmk.modules.mouse_keys import MouseKeys
    from kmk.modules.layers import Layers
    keyboard.modules = [
        split,
        power,
        HoldTap(),
        MouseKeys(),
        Layers()
    ]         
    return keyboard            

def clear_bonds():
    import _bleio
    _bleio.adapter.erase_bonding()        

bleEnabled = isItOn(col_pins, row_pins, bleSelectButton)
resetBondsTestA = isItOn(col_pins, row_pins, 0)
resetBondsTestB = isItOn(col_pins, row_pins, 12)
print("resetBondsTestA", resetBondsTestA)
print("resetBondsTestB", resetBondsTestB)
if resetBondsTestA and resetBondsTestB:
    clear_bonds()
    print("Bonds cleared")


    
print("BLE ENABLED", bleEnabled)
def assignKeymap(kb):
    from keyAssignations import assignKeys
    kb.keymap = assignKeys()
    
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

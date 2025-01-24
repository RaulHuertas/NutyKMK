
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
def initKB():
    from nkbusb import NKB_USB, USBFeedback
    from kmk.modules.splituart import SplitUART, SplitSide
    keyboard = NKB_USB(col_pins, row_pins)
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
    split = SplitUART(
            split_side=SplitSide.LEFT,
            split_target_left=False,
            data_pin = board.NFC1,#RX
            data_pin2 = board.NFC2,#TX
            debug_enabled = testing
        )
    keyboard.modules = [
        split, 
        USBFeedback(board.D0, 24,brightness=0.1)
    ]

    
    return keyboard

def assignKeymap(kb):
    from keyAssignations import assignKeys
    kb.keymap = assignKeys()
    
if __name__ == '__main__':
    keyboard = initKB()
    assignKeymap(keyboard)
    keyboard.debug_enabled = testing
    keyboard.go()

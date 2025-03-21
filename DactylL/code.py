
print("Starting on SHIRIL")



testing = True

def initKB():
    
    import board
    global testing
    col_pins = (board.NFC1,board.NFC2,board.D7,board.D8, board.D9,board.D10 ,)
    row_pins = (board.D2, board.D3, board.D4,board.D5,board.D6,)

    from nkbble import NKB_BLE, BLEFeedback
    keyboard = NKB_BLE(row_pins=row_pins, col_pins=col_pins)
    lightsFeedback = BLEFeedback()
    keyboard.modules.append(lightsFeedback)
    from kmk.modules.splitbl import SplitBL, SplitSide, SplitRole
    split = SplitBL(
        split_side=SplitSide.LEFT,
        split_role=SplitRole.Secondary,
        debug_enabled=testing
    )
    keyboard.modules.append(split)
    from kmk.modules.power import Power    
    power = Power()
    keyboard.modules.append(power)
    


    keyboard.coord_mapping =  [
        0,  1,  2,  3,  4,  5, 
        24, 25, 26, 27, 28, 29,
        6,  7,  8,  9, 10, 11,
        30, 31, 32, 33, 34, 35,
        12, 13, 14, 15, 16, 17,
        36, 37, 38, 39, 40, 41,
        18, 19, 20, 21, 22, 23,
        42, 43, 44, 45, 46, 47,
        24, 25, 26, 27, 28, 29,
        48, 49, 50, 51, 52, 53,
        30, 31, 32, 33, 34, 35,
        54, 55, 56, 57, 58, 59,
    ]

    
    import gc
    gc.collect()
   
    return keyboard


if __name__ == '__main__':
    print("Starting on SHIRIL now")
    kb = initKB()
    kb.debug_enabled = True

    
    from keyAssignationsBLE import assignKeys
    kb.keymap = assignKeys()
    del assignKeys
    kb.powersave_enable = True    
    kb.go( )




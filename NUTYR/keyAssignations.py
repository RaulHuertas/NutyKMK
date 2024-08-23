from kmk.keys import KC
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.layers import Layers
from kmk.modules.mouse_keys import MouseKeys

class ESKeycodes:
    NTIL = KC.SCOLON
    OPENING_QUESTION_MARK  = KC.EQUAL
    QUOTE  = KC.MINUS
    OPENING_BRAQUETS  = KC.QUOTE    
    CLOSING_BRAQUETS  = KC.NONUS_HASH 
    LESSER_GREATER = KC.NUBS
    TILDE_DIERESIS = KC.LBRACKET
    PLUS = KC.RBRACKET
    PIPE = KC.GRAVE 
    
    

def assignKeys ():
    
    
    layer0Asignations = [ KC.NO]*48
    #return [layer0Asignations]
    #ROW0
    layer0Asignations[0] =  KC.TAB
    layer0Asignations[1] =  KC.Q
    layer0Asignations[2] =  KC.W
    layer0Asignations[3] =  KC.E
    layer0Asignations[4] =  KC.R
    layer0Asignations[5] =  KC.T
    layer0Asignations[6] =  KC.Y
    layer0Asignations[7] =   KC.U
    layer0Asignations[8] =   KC.I
    layer0Asignations[9] =  KC.O
    layer0Asignations[10] =  KC.P
    layer0Asignations[11] =   KC.BSPACE
    #ROW1
    layer0Asignations[12] =  KC.LSHIFT
    layer0Asignations[13] =  KC.A
    layer0Asignations[14] =  KC.S
    layer0Asignations[15] =  KC.D
    layer0Asignations[16] =  KC.F
    layer0Asignations[17] =  KC.G
    layer0Asignations[18] =  KC.H
    layer0Asignations[19] =  KC.J
    layer0Asignations[20] =  KC.K
    layer0Asignations[21] =  KC.L
    layer0Asignations[22] =  ESKeycodes.NTIL
    layer0Asignations[23] =  ESKeycodes.TILDE_DIERESIS
    #ROW2

    layer0Asignations[24] =  KC.LCTRL
    layer0Asignations[25] =  KC.Z
    layer0Asignations[26] =  KC.X
    layer0Asignations[27] =  KC.C
    layer0Asignations[28] =  KC.V
    layer0Asignations[29] =  KC.B
    layer0Asignations[30] =  KC.N
    layer0Asignations[31] =  KC.M
    layer0Asignations[32] =  KC.COMMA
    layer0Asignations[33] =  KC.DOT
    layer0Asignations[34] =  KC.SLASH
    layer0Asignations[35] =  KC.FD(1)
    #ROW3
    layer0Asignations[36] =  KC.NO
    layer0Asignations[37] =  KC.NO
    layer0Asignations[38] =  KC.AUDIO_MUTE
    layer0Asignations[39] =  KC.LALT # KC.TD( KC.BSPACE, KC.DELETE, tap_time=tapTime)
    layer0Asignations[40] =  KC.SPACE
    layer0Asignations[41] =  KC.MO(1)

    
    layer0Asignations[42] =  KC.LGUI
    layer0Asignations[43] =  KC.ENTER
    layer0Asignations[44] =  KC.ESCAPE
    layer0Asignations[45] =  KC.NO
    layer0Asignations[46] =  KC.NO
    layer0Asignations[47] =  KC.NO


    layer1Asignations = [ KC.NO]*48
    #ROW0
    layer1Asignations[0] =  KC.TAB
    layer1Asignations[1] =  KC.PSCREEN
    layer1Asignations[2] =  KC.HOME
    layer1Asignations[3] =  KC.END    
    layer1Asignations[4] =  ESKeycodes.OPENING_BRAQUETS   
    layer1Asignations[5] =  ESKeycodes.PLUS

    layer1Asignations[6] =   KC.N6
    layer1Asignations[7] =  KC.N7 
    layer1Asignations[8] =  KC.N8
    layer1Asignations[9] =  KC.N9
    layer1Asignations[10] =  KC.N0
    layer1Asignations[11] =   KC.DELETE
    #ROW1
    layer1Asignations[12] =  KC.LSHIFT
    layer1Asignations[13] =  KC.RALT
    layer1Asignations[14] =  ESKeycodes.OPENING_QUESTION_MARK  
    layer1Asignations[15] = ESKeycodes.QUOTE  
    layer1Asignations[16] =  ESKeycodes.CLOSING_BRAQUETS 
    layer1Asignations[17] =  KC.F1

    layer1Asignations[18] =  KC.LEFT
    layer1Asignations[19] =  KC.DOWN
    layer1Asignations[20] =  KC.UP
    layer1Asignations[21] =  KC.RIGHT
    layer1Asignations[22] =  ESKeycodes.LESSER_GREATER
    layer1Asignations[23] =   ESKeycodes.PIPE
    
    #ROW2
    layer1Asignations[24] =  KC.LCTRL
    layer1Asignations[25] =  KC.F5
    layer1Asignations[26] =  KC.F9
    layer1Asignations[27] =  KC.F10
    layer1Asignations[28] =  KC.F11
    layer1Asignations[29] =  KC.F12

    layer1Asignations[30] = KC.N1
    layer1Asignations[31] =  KC.N2
    layer1Asignations[32] =  KC.N3
    layer1Asignations[33] =  KC.N4
    layer1Asignations[34] =  KC.N5
    layer1Asignations[35] =  KC.FD(2)
    #ROW3
    layer1Asignations[36] =  KC.NO
    layer1Asignations[37] =  KC.NO
    layer1Asignations[38] =  KC.NO
    layer1Asignations[39] =  KC.LALT
    layer1Asignations[40] =  KC.MO(2)
    layer1Asignations[41] =  KC.FD(0)

    layer1Asignations[42] =  KC.LGUI
    layer1Asignations[43] =  KC.ENTER
    layer1Asignations[44] =  KC.APPLICATION
    layer1Asignations[45] =  KC.NO
    layer1Asignations[46] =  KC.NO
    layer1Asignations[47] =  KC.NO


    layer2Asignations = [ KC.NO]*48
    #ROW0
    layer2Asignations[0] =  KC.TAB
    layer2Asignations[1] =  KC.PSCREEN
    layer2Asignations[2] =  KC.INSERT
    layer2Asignations[3] =  KC.HOME
    layer2Asignations[4] =  KC.PGUP
    layer2Asignations[5] =  KC.NO

    layer2Asignations[6] =  KC.MB_LMB
    layer2Asignations[7] =  KC.MB_RMB
    layer2Asignations[8] =  KC.MB_MMB
    layer2Asignations[9] =  KC.NO
    layer2Asignations[10] =  KC.AUDIO_MUTE
    layer2Asignations[11] =   KC.AUDIO_VOL_UP
    #ROW1
    layer2Asignations[12] =  KC.LSHIFT
    layer2Asignations[13] =  KC.RALT
    layer2Asignations[14] =  KC.DELETE
    layer2Asignations[15] =  KC.END
    layer2Asignations[16] =  KC.PGDOWN
    layer2Asignations[17] =  KC.NO

    layer2Asignations[18] =  KC.MB_LMB
    layer2Asignations[19] =  KC.MB_RMB
    layer2Asignations[20] =  KC.MB_MMB
    layer2Asignations[21] =  KC.NO
    layer2Asignations[22] =  KC.F2
    layer2Asignations[23] =   KC.AUDIO_VOL_DOWN
    
    #ROW2
    layer2Asignations[24] =  KC.LCTRL
    layer2Asignations[25] =  KC.NO
    layer2Asignations[26] =  KC.NO
    layer2Asignations[27] =  KC.NO
    layer2Asignations[28] = KC.NO
    layer2Asignations[29] =  KC.NO

    layer2Asignations[30] =  KC.F3
    layer2Asignations[31] =  KC.F4
    layer2Asignations[32] =  KC.F6
    layer2Asignations[33] =  KC.F7
    layer2Asignations[34] =  KC.F8
    layer2Asignations[35] =  KC.FD(0)
    #ROW3
    layer2Asignations[36] =  KC.NO
    layer2Asignations[37] =  KC.NO
    layer2Asignations[38] =  KC.NO
    layer2Asignations[39] =  KC.LALT
    layer2Asignations[40] =  KC.SPACE
    layer2Asignations[41] =  KC.FD(0)

    layer2Asignations[42] =  KC.LGUI
    layer2Asignations[43] =  KC.ENTER
    layer2Asignations[44] =  KC.FD(0)
    layer2Asignations[45] =  KC.NO
    layer2Asignations[46] =  KC.NO
    layer2Asignations[47] =  KC.NO


    return  [
        layer0Asignations,#base
        layer1Asignations,#nums and symbols
        layer2Asignations,#FN ,#nums and symbols
    ]


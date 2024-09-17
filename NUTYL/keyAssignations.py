from kmk.keys import KC
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.layers import Layers
from kmk.modules.mouse_keys import MouseKeys

#class ESKeycodes:

def assignKeys ():
    NTIL = KC.SCOLON
    OPENING_QUESTION_MARK  = KC.EQUAL
    QUOTE  = KC.MINUS
    OPENING_BRAQUETS  = KC.QUOTE    
    CLOSING_BRAQUETS  = KC.NONUS_HASH 
    LESSER_GREATER = KC.NUBS
    TILDE_DIERESIS = KC.LBRACKET
    PLUS = KC.RBRACKET
    PIPE = KC.GRAVE 
    
    kc = KC
    goHome = kc.FD(0)
    noAsg = kc.NO
    lShift = kc.LSHIFT



    
    layer0Asignations = [ noAsg]*48
    #return [layer0Asignations]
    #ROW0
    layer0Asignations[0] =  kc.TAB
    layer0Asignations[1] =  kc.Q
    layer0Asignations[2] =  kc.W
    layer0Asignations[3] =  kc.E
    layer0Asignations[4] =  kc.R
    layer0Asignations[5] =  kc.T
    layer0Asignations[6] =  kc.Y
    layer0Asignations[7] =   kc.U
    layer0Asignations[8] =   kc.I
    layer0Asignations[9] =  kc.O
    layer0Asignations[10] =  kc.P
    layer0Asignations[11] =   kc.BSPACE
    #ROW1
    layer0Asignations[12] =  lShift
    layer0Asignations[13] =  kc.A
    layer0Asignations[14] =  kc.S
    layer0Asignations[15] =  kc.D
    layer0Asignations[16] =  kc.F
    layer0Asignations[17] =  kc.G
    layer0Asignations[18] =  kc.H
    layer0Asignations[19] =  kc.J
    layer0Asignations[20] =  kc.K
    layer0Asignations[21] =  kc.L
    layer0Asignations[22] =  NTIL
    layer0Asignations[23] =  TILDE_DIERESIS
    #ROW2

    layer0Asignations[24] =  kc.LCTRL
    layer0Asignations[25] =  kc.Z
    layer0Asignations[26] =  kc.X
    layer0Asignations[27] =  kc.C
    layer0Asignations[28] =  kc.V
    layer0Asignations[29] =  kc.B
    layer0Asignations[30] =  kc.N
    layer0Asignations[31] =  kc.M
    layer0Asignations[32] =  kc.COMMA
    layer0Asignations[33] =  kc.DOT
    layer0Asignations[34] =  kc.SLASH
    layer0Asignations[35] =  kc.FD(1)
    #ROW3
    layer0Asignations[36] =  kc.LALT # kc.TD( kc.BSPACE, kc.DELETE, tap_time=tapTime)
    layer0Asignations[37] =  kc.SPACE
    layer0Asignations[38] =  kc.MO(1)
    layer0Asignations[39] =  noAsg
    layer0Asignations[40] =  noAsg
    layer0Asignations[41] =  noAsg

    
    
    layer0Asignations[42] =  noAsg
    layer0Asignations[43] =  noAsg
    layer0Asignations[44] =  noAsg
    layer0Asignations[45] =  kc.LGUI
    layer0Asignations[46] =  kc.ENTER
    layer0Asignations[47] =  kc.ESCAPE


    layer1Asignations = [ noAsg]*48
    #ROW0
    layer1Asignations[0] =  kc.TAB
    layer1Asignations[1] =  kc.PSCREEN
    layer1Asignations[2] =  kc.HOME
    layer1Asignations[3] =  kc.END    
    layer1Asignations[4] =  OPENING_BRAQUETS   
    layer1Asignations[5] =  PLUS

    layer1Asignations[6] =   kc.N6
    layer1Asignations[7] =  kc.N7 
    layer1Asignations[8] =  kc.N8
    layer1Asignations[9] =  kc.N9
    layer1Asignations[10] =  kc.N0
    layer1Asignations[11] =   kc.DELETE
    #ROW1
    layer1Asignations[12] =  lShift
    layer1Asignations[13] =  kc.RALT
    layer1Asignations[14] =  OPENING_QUESTION_MARK  
    layer1Asignations[15] = QUOTE  
    layer1Asignations[16] =  CLOSING_BRAQUETS 
    layer1Asignations[17] =  kc.F1

    layer1Asignations[18] =  kc.LEFT
    layer1Asignations[19] =  kc.DOWN
    layer1Asignations[20] =  kc.UP
    layer1Asignations[21] =  kc.RIGHT
    layer1Asignations[22] =  LESSER_GREATER
    layer1Asignations[23] =   PIPE
    
    #ROW2
    layer1Asignations[24] =  kc.LCTRL
    layer1Asignations[25] =  kc.F5
    layer1Asignations[26] =  kc.F9
    layer1Asignations[27] =  kc.F10
    layer1Asignations[28] =  kc.F11
    layer1Asignations[29] =  kc.F12

    layer1Asignations[30] = kc.N1
    layer1Asignations[31] =  kc.N2
    layer1Asignations[32] =  kc.N3
    layer1Asignations[33] =  kc.N4
    layer1Asignations[34] =  kc.N5
    layer1Asignations[35] =  kc.FD(2)
    #ROW3
    layer1Asignations[36] =  noAsg
    layer1Asignations[37] =  noAsg
    layer1Asignations[38] =  noAsg
    layer1Asignations[39] =  kc.LALT
    layer1Asignations[40] =  kc.MO(2)
    layer1Asignations[41] =  goHome

    layer1Asignations[42] =  kc.LGUI
    layer1Asignations[43] =  kc.ENTER
    layer1Asignations[44] =  kc.APPLICATION
    layer1Asignations[45] =  noAsg
    layer1Asignations[46] =  noAsg
    layer1Asignations[47] =  noAsg


    layer2Asignations = [ noAsg]*48
    #ROW0
    layer2Asignations[0] =  kc.TAB
    layer2Asignations[1] =  kc.PSCREEN
    layer2Asignations[2] =  kc.INSERT
    layer2Asignations[3] =  kc.HOME
    layer2Asignations[4] =  kc.PGUP
    layer2Asignations[5] =  noAsg

    layer2Asignations[6] =  kc.MB_LMB
    layer2Asignations[7] =  kc.MB_RMB
    layer2Asignations[8] =  kc.MB_MMB
    layer2Asignations[9] =  noAsg
    layer2Asignations[10] =  kc.AUDIO_MUTE
    layer2Asignations[11] =   kc.AUDIO_VOL_UP
    #ROW1
    layer2Asignations[12] =  lShift
    layer2Asignations[13] =  kc.RALT
    layer2Asignations[14] =  kc.DELETE
    layer2Asignations[15] =  kc.END
    layer2Asignations[16] =  kc.PGDOWN
    layer2Asignations[17] =  noAsg

    layer2Asignations[18] =  kc.MB_LMB
    layer2Asignations[19] =  kc.MB_RMB
    layer2Asignations[20] =  kc.MB_MMB
    layer2Asignations[21] =  noAsg
    layer2Asignations[22] =  kc.F2
    layer2Asignations[23] =   kc.AUDIO_VOL_DOWN
    
    #ROW2
    layer2Asignations[24] =  kc.LCTRL
    layer2Asignations[25] =  noAsg
    layer2Asignations[26] =  noAsg
    layer2Asignations[27] =  noAsg
    layer2Asignations[28] = noAsg
    layer2Asignations[29] =  noAsg

    layer2Asignations[30] =  kc.F3
    layer2Asignations[31] =  kc.F4
    layer2Asignations[32] =  kc.F6
    layer2Asignations[33] =  kc.F7
    layer2Asignations[34] =  kc.F8
    layer2Asignations[35] =  goHome
    #ROW3
    layer2Asignations[36] =  noAsg
    layer2Asignations[37] =  noAsg
    layer2Asignations[38] =  noAsg
    layer2Asignations[39] =  kc.LALT
    layer2Asignations[40] =  kc.SPACE
    layer2Asignations[41] =  goHome

    layer2Asignations[42] =  kc.LGUI
    layer2Asignations[43] =  kc.ENTER
    layer2Asignations[44] =  goHome
    layer2Asignations[45] =  noAsg
    layer2Asignations[46] =  noAsg
    layer2Asignations[47] =  noAsg


    return  [
        layer0Asignations,#base
        layer1Asignations,#nums and symbols
        layer2Asignations,#FN ,#nums and symbols
    ]


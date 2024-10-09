from kmk.keys import KC
from snKeycodes import ESKeycodes
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.layers import Layers
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.tapdance import TapDance



tapTime = 400
velocity = 64
def assignKeys ():
    
    
    layer0Asignations = [ KC.NO]*48
    #return [layer0Asignations]
    #ROW0
    layer0Asignations[0] =  KC.ESCAPE
    layer0Asignations[1] =  KC.Q
    layer0Asignations[2] =  KC.W
    layer0Asignations[3] =  KC.E
    layer0Asignations[4] =  KC.R
    layer0Asignations[5] =  KC.T
    layer0Asignations[6] =  KC.Y
    layer0Asignations[7] =  KC.U
    layer0Asignations[8] =  KC.I
    layer0Asignations[9] =  KC.O
    layer0Asignations[10] =  KC.P
    layer0Asignations[11] =  KC.BACKSPACE
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
    layer0Asignations[23] =  KC.TD(KC.FD(3), KC.FD(0), tap_time=tapTime)
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
    layer0Asignations[35] =  KC.LALT
    #ROW3
    layer0Asignations[36] =  KC.NO
    layer0Asignations[37] =  KC.NO
    layer0Asignations[38] =  KC.NO
    layer0Asignations[39] =   KC.TD(KC.FD(1), KC.FD(0), tap_time=tapTime)

    layer0Asignations[40] =  KC.SPACE
    layer0Asignations[41] =  KC.LGUI
    layer0Asignations[42] = KC.TD(KC.FD(2), KC.FD(0), tap_time=tapTime)
    layer0Asignations[43] =  KC.ENTER
    layer0Asignations[44] =  KC.TAB
    layer0Asignations[45] =  KC.NO
    layer0Asignations[46] =  KC.NO
    layer0Asignations[47] =  KC.NO


    layer1Asignations = [ KC.TRANSPARENT]*48
    #ROW0
    layer1Asignations[0] =  KC.ESCAPE
    layer1Asignations[1] =  KC.PSCREEN
    layer1Asignations[2] =  ESKeycodes.TILDE_DIERESIS
    layer1Asignations[3] =  KC.UP
    layer1Asignations[4] =  ESKeycodes.OPENING_QUESTION_MARK
    layer1Asignations[5] =  ESKeycodes.QUOTE
    layer1Asignations[6] =  ESKeycodes.OPENING_BRAQUETS
    layer1Asignations[7] =  ESKeycodes.CLOSING_BRAQUETS
    layer1Asignations[8] =  KC.N7
    layer1Asignations[9] =  KC.N8
    layer1Asignations[10] =  KC.N9
    layer1Asignations[11] =  KC.BSPACE
    #ROW1
    layer1Asignations[12] =  KC.LSHIFT
    layer1Asignations[13] =  ESKeycodes.LESSER_GREATER
    layer1Asignations[14] =  KC.LEFT
    layer1Asignations[15] =  KC.DOWN
    layer1Asignations[16] =  KC.RIGHT
    layer1Asignations[17] =  ESKeycodes.PIPE
    layer1Asignations[18] =  KC.F12
    layer1Asignations[19] =  ESKeycodes.PLUS
    layer1Asignations[20] =  KC.N4
    layer1Asignations[21] =  KC.N5
    layer1Asignations[22] =  KC.N6
    layer1Asignations[23] =   KC.TD(KC.FD(3), KC.FD(0), tap_time=tapTime)
    
    #ROW2
    layer1Asignations[24] =  KC.LCTRL
    layer1Asignations[25] =  KC.AUDIO_VOL_DOWN
    layer1Asignations[26] =  KC.AUDIO_VOL_UP
    layer1Asignations[27] =  KC.AUDIO_MUTE
    layer1Asignations[28] =  KC.NO
    layer1Asignations[29] =  KC.NO
    layer1Asignations[30] =  KC.F11
    layer1Asignations[31] =  KC.N0
    layer1Asignations[32] =  KC.N1
    layer1Asignations[33] =  KC.N2
    layer1Asignations[34] =  KC.N3
    layer1Asignations[35] =  KC.LALT
    #ROW3
    layer1Asignations[36] =  KC.TRANSPARENT
    layer1Asignations[37] =  KC.TRANSPARENT
    layer1Asignations[38] =  KC.TRANSPARENT
    layer1Asignations[39] =   KC.TD(KC.FD(1), KC.FD(0), tap_time=tapTime)
    layer1Asignations[40] =  KC.TRANSPARENT
    layer1Asignations[41] =  KC.TRANSPARENT
    layer1Asignations[42] =  KC.TD(KC.FD(2), KC.FD(0), tap_time=tapTime)
    layer1Asignations[43] =  KC.ENTER
    layer1Asignations[44] =  KC.TRANSPARENT
    layer1Asignations[45] =  KC.TRANSPARENT
    layer1Asignations[46] =  KC.TRANSPARENT
    layer1Asignations[47] =  KC.TRANSPARENT


    layer2Asignations = [ KC.TRANSPARENT]*48
    #ROW0
    layer2Asignations[0] =  KC.ESCAPE
    layer2Asignations[1] =  KC.TRANSPARENT
    layer2Asignations[2] =  KC.TRANSPARENT
    layer2Asignations[3] =  KC.TRANSPARENT
    layer2Asignations[4] =  ESKeycodes.OPENING_QUESTION_MARK
    layer2Asignations[5] =  ESKeycodes.QUOTE
    layer2Asignations[6] =  ESKeycodes.OPENING_BRAQUETS
    layer2Asignations[7] =  KC.MB_LMB
    layer2Asignations[8] =  KC.MS_UP
    layer2Asignations[9] =  KC.TRANSPARENT
    layer2Asignations[10] =  KC.HOME
    layer2Asignations[11] =  KC.PGUP
    #ROW1
    layer2Asignations[12] =  KC.LSHIFT
    layer2Asignations[13] =  KC.F6
    layer2Asignations[14] =  KC.F7
    layer2Asignations[15] =  KC.F8
    layer2Asignations[16] =  KC.F9
    layer2Asignations[17] =  KC.F10
    layer2Asignations[18] =  KC.F12
    layer2Asignations[19] =  KC.MS_LEFT
    layer2Asignations[20] =  KC.MS_DOWN
    layer2Asignations[21] =  KC.MS_RIGHT
    layer2Asignations[22] =  KC.END
    layer2Asignations[23] =  KC.PGDOWN
    
    #ROW2
    layer2Asignations[24] =  KC.LCTRL
    layer2Asignations[25] =  KC.F1
    layer2Asignations[26] =  KC.F2
    layer2Asignations[27] =  KC.F3
    layer2Asignations[28] =  KC.F4
    layer2Asignations[29] =  KC.F5
    layer2Asignations[30] =  KC.F11
    layer2Asignations[31] =  KC.TRANSPARENT
    layer2Asignations[32] =  KC.TRANSPARENT
    layer2Asignations[33] =  KC.TRANSPARENT
    layer2Asignations[34] =  KC.TRANSPARENT
    layer2Asignations[35] =  KC.LALT
    #ROW3
    layer2Asignations[36] =  KC.TRANSPARENT
    layer2Asignations[37] =  KC.TRANSPARENT
    layer2Asignations[38] =  KC.TRANSPARENT
    layer2Asignations[39] =  KC.TD(KC.FD(1), KC.FD(0), tap_time=tapTime)
    layer2Asignations[40] =  KC.TRANSPARENT
    layer2Asignations[41] =  KC.TRANSPARENT
    layer2Asignations[42] =   KC.TD(KC.FD(0), KC.FD(0), tap_time=tapTime)
    layer2Asignations[43] =  KC.ENTER
    layer2Asignations[44] =  KC.TRANSPARENT
    layer2Asignations[45] =  KC.TRANSPARENT
    layer2Asignations[46] =  KC.TRANSPARENT
    layer2Asignations[47] =  KC.TRANSPARENT


    layer3Asignations = [ KC.TRANSPARENT]*48
    #ROW0
    layer3Asignations[0] =  KC.MIDI_NOTE(48, velocity)
    layer3Asignations[1] =  KC.MIDI_NOTE(49, velocity)
    layer3Asignations[2] =  KC.MIDI_NOTE(50,velocity)
    layer3Asignations[3] =  KC.MIDI_NOTE(51, velocity)
    layer3Asignations[4] =  KC.MIDI_NOTE(52, velocity)
    layer3Asignations[5] =  KC.MIDI_NOTE(53,velocity)
    layer3Asignations[6] =  KC.MIDI_NOTE(54, velocity)
    layer3Asignations[7] =  KC.MIDI_NOTE(55, velocity)
    layer3Asignations[8] =  KC.MIDI_NOTE(56, velocity)
    layer3Asignations[9] =  KC.MIDI_NOTE(57, velocity)
    layer3Asignations[10] =  KC.MIDI_NOTE(58, velocity)
    layer3Asignations[11] =  KC.MIDI_NOTE(59, velocity)
    #ROW1
    layer3Asignations[12] =  KC.MIDI_NOTE(60, velocity)
    layer3Asignations[13] =  KC.MIDI_NOTE(61, velocity)
    layer3Asignations[14] =  KC.MIDI_NOTE(62, velocity)
    layer3Asignations[15] =  KC.MIDI_NOTE(63, velocity)
    layer3Asignations[16] =  KC.MIDI_NOTE(64, velocity)
    layer3Asignations[17] =  KC.MIDI_NOTE(65,velocity)
    layer3Asignations[18] =  KC.MIDI_NOTE(66, velocity)
    layer3Asignations[19] =  KC.MIDI_NOTE(67, velocity)
    layer3Asignations[20] =  KC.MIDI_NOTE(68,velocity)
    layer3Asignations[21] =  KC.MIDI_NOTE(69,velocity)
    layer3Asignations[22] =  KC.MIDI_NOTE(70, velocity)
    layer3Asignations[23] =  KC.MIDI_NOTE(71, velocity)
    
    #ROW2
    layer3Asignations[24] =  KC.MIDI_NOTE(72,velocity)
    layer3Asignations[25] =  KC.MIDI_NOTE(73, velocity)
    layer3Asignations[26] =  KC.MIDI_NOTE(74,velocity)
    layer3Asignations[27] =  KC.MIDI_NOTE(75, velocity)
    layer3Asignations[28] =  KC.MIDI_NOTE(76, velocity)
    layer3Asignations[29] =  KC.MIDI_NOTE(77, velocity)
    layer3Asignations[30] =  KC.MIDI_NOTE(78, velocity)
    layer3Asignations[31] =  KC.MIDI_NOTE(79, velocity)
    layer3Asignations[32] =  KC.MIDI_NOTE(80, velocity)
    layer3Asignations[33] =  KC.MIDI_NOTE(81, velocity)
    layer3Asignations[34] =  KC.MIDI_NOTE(82, velocity)
    layer3Asignations[35] =  KC.MIDI_NOTE(83, velocity)
    #ROW3
    layer3Asignations[36] =  KC.TRANSPARENT
    layer3Asignations[37] =  KC.TRANSPARENT
    layer3Asignations[38] =  KC.TRANSPARENT
    layer3Asignations[39] =  KC.TD(KC.FD(1), KC.FD(0), tap_time=tapTime)
    layer3Asignations[40] =  KC.TRANSPARENT
    layer3Asignations[41] =  KC.TRANSPARENT
    layer3Asignations[42] =   KC.TD(KC.FD(2), KC.FD(0), tap_time=tapTime)
    layer3Asignations[43] =  KC.ENTER
    layer3Asignations[44] =  KC.TRANSPARENT
    layer3Asignations[45] =  KC.TRANSPARENT
    layer3Asignations[46] =  KC.TRANSPARENT
    layer3Asignations[47] =  KC.TRANSPARENT

    return  [
        layer0Asignations,#base
        layer1Asignations,#nums and symbols
        layer2Asignations,#FN and mouse,#nums and symbols
        layer3Asignations,#midi
    ]




from kmk.keys import KC

def assignKeys ():
    
    
   
        
    kc = KC
    noAsg = kc.NO
    esc = kc.ESCAPE
    #SPANISH UNITED STATES INTERNATIONAL
    comilla_simple = kc.MINUS 
    exclam_ap = kc.EQUAL 
    degrees = kc.GRAVE
    ntil = kc.SCOLON
    lesser_greater = kc.NUBS
    dash = KC.SLASH
    
    mas = kc.RBRACKET
    tildeInvertida = kc.LBRACKET
    tilde =  kc.QUOTE
    cCedilla =  kc.BSLASH
    
    
    goHome = kc.FD(0)
    layer1 = kc.FD(1)
    layer2 = kc.FD(2)
    temporalLayer1 = kc.MO(1)

    keysNumber = 60

    layer0Asignations = [ noAsg]*keysNumber
    layer0Asignations[0] = esc
    layer0Asignations[1] = kc.N1
    layer0Asignations[2] = kc.N2
    layer0Asignations[3] = kc.N3
    layer0Asignations[4] = kc.N4
    layer0Asignations[5] = kc.N5    
    layer0Asignations[6] = kc.N6
    layer0Asignations[7] = kc.N7
    layer0Asignations[8] = kc.N8
    layer0Asignations[9] = kc.N9
    layer0Asignations[10] = kc.N0
    layer0Asignations[11] = exclam_ap

    layer0Asignations[12] = kc.TAB
    layer0Asignations[13] = kc.Q
    layer0Asignations[14] = kc.W
    layer0Asignations[15] = kc.E
    layer0Asignations[16] = kc.R
    layer0Asignations[17] = kc.T    
    layer0Asignations[18] = kc.Y
    layer0Asignations[19] = kc.U
    layer0Asignations[20] = kc.I
    layer0Asignations[21] = kc.O
    layer0Asignations[22] = kc.P
    layer0Asignations[23] = comilla_simple

    layer0Asignations[24] = degrees
    layer0Asignations[25] = kc.A
    layer0Asignations[26] = kc.S
    layer0Asignations[27] = kc.D
    layer0Asignations[28] = kc.F
    layer0Asignations[29] = kc.G    
    layer0Asignations[30] = kc.H
    layer0Asignations[31] = kc.J
    layer0Asignations[32] = kc.K
    layer0Asignations[33] = kc.L
    layer0Asignations[34] = ntil
    layer0Asignations[35] = tildeInvertida

    layer0Asignations[36] = lesser_greater
    layer0Asignations[37] = kc.Z
    layer0Asignations[38] = kc.X
    layer0Asignations[39] = kc.C
    layer0Asignations[40] = kc.V
    layer0Asignations[41] = kc.B    
    layer0Asignations[42] = kc.N
    layer0Asignations[43] = kc.M
    layer0Asignations[44] = kc.COMMA
    layer0Asignations[45] = kc.DOT
    layer0Asignations[46] = dash
    layer0Asignations[47] = mas


    
    layer0Asignations[48] =cCedilla 
    layer0Asignations[49] = tilde
    layer0Asignations[50] = kc.SPACE
    layer0Asignations[51] = KC.RALT
    layer0Asignations[52] = temporalLayer1
    layer0Asignations[53] = kc.LCTRL        
    layer0Asignations[54] = kc.LGUI
    layer0Asignations[55] = kc.LALT
    layer0Asignations[56] = kc.LSHIFT
    layer0Asignations[57] = goHome
    layer0Asignations[58] = kc.BSPACE
    layer0Asignations[59] = kc.ENTER

    layer1Asignations = [ noAsg]*keysNumber   
    layer1Asignations[58] = kc.DELETE

    layer2Asignations = [ noAsg]*keysNumber
    return  [
        layer0Asignations,#base
        layer1Asignations,#nums and symbols
        layer2Asignations
    ]


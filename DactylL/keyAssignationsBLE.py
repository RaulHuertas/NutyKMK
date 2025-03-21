

def assignKeys ():
    from kmk.keys import KC
    nKeys = 60    
    kc = KC
    NTIL = kc.SCOLON
    OPENING_QUESTION_MARK  = kc.EQUAL
    QUOTE  = kc.MINUS
    OPENING_BRAQUETS  = kc.QUOTE    
    CLOSING_BRAQUETS  = kc.NONUS_HASH 
    LESSER_GREATER = kc.NUBS
    TILDE_DIERESIS = kc.LBRACKET
    PLUS = kc.RBRACKET
    PIPE = kc.GRAVE 
    space = kc.SPACE
    goHome = kc.FD(0)
    noAsg = kc.NO
    lShift = kc.LSHIFT
    layer1 = kc.FD(1)
    layer2 = kc.FD(2)
    esc = kc.ESCAPE

    layer0Asignations = [ noAsg]*60

    layer1Asignations = [ noAsg]*60
    #ROW0
    layer2Asignations = [ noAsg]*60

    return  [
        layer0Asignations,#base
        layer1Asignations,#nums and symbols
        layer2Asignations
    ]


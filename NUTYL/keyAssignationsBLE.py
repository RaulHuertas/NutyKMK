

def assignKeys ():
    from kmk.keys import KC
    
    kc = KC
    goHome = kc.FD(0)
    noAsg = kc.NO
    layer1 = kc.FD(1)
    layer2 = kc.FD(2)

    layer0Asignations = [ noAsg]*48
    layer0Asignations[35] =  layer1
    layer0Asignations[38] =  kc.MO(1)

    layer1Asignations = [ noAsg]*48
    layer1Asignations[35] =  layer2
    layer1Asignations[38] =  goHome


    layer2Asignations = [ noAsg]*48
    layer2Asignations[38] =  goHome

    
    return  [
        layer0Asignations,#base
        layer1Asignations,#nums and symbols
        layer2Asignations
    ]


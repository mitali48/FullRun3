# structure configuration for datacard

structure = {}

# keys here must match keys in samples.py    
structure['DY'] = {   
    'isSignal' : 0,
    'isData'   : 0 
}

structure['Top'] = {   
    'isSignal' : 0,
    'isData'   : 0 
}

structure['WZ'] = {   
    'isSignal' : 0,
    'isData'   : 0 
}

structure['ZZ'] = {   
    'isSignal' : 0,
    'isData'   : 0 
}

structure['Zg'] = {   
    'isSignal' : 0,
    'isData'   : 0 
}

structure['Wg'] = {   
    'isSignal' : 0,
    'isData'   : 0 
}

structure['ZgS'] = {   
    'isSignal' : 0,
    'isData'   : 0 
}

structure['WgS'] = {   
    'isSignal' : 0,
    'isData'   : 0 
}

structure['VVV'] = {   
    'isSignal' : 0,
    'isData'   : 0 
}

structure['ggF'] = {   
    'isSignal' : 0,
    'isData'   : 0 
}

structure['VBF'] = {   
    'isSignal' : 0,
    'isData'   : 0 
}

structure['ggH_hww'] = {   
    'isSignal' : 0,
    'isData'   : 0 
}

structure['qqH_hww'] = {   
    'isSignal' : 0,
    'isData'   : 0 
}


#signal

structure['ggWW'] = {   
    'isSignal' : 1,
    'isData'   : 0 
}

structure['WW'] = {   
    'isSignal' : 1,
    'isData'   : 0 
}

#fakes
structure['Fake'] = {   
    'isSignal' : 0,
    'isData'   : 0 
}

# data
structure['DATA']  = { 
    'isSignal' : 0,
    'isData'   : 1 
}


# for nuis in nuisances.values():
#     if 'cutspost' in nuis:
#         print(nuis)
#         nuis['cuts'] = nuis['cutspost']
#         print(nuis)
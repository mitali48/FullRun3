# structure configuration for datacard

structure = {}



structure['DY'] = {
    'isSignal' : 0,
    'isData'   : 0
    }

structure['top'] = {
    'isSignal' : 0,
    'isData'   : 0
    }

structure['ggWW'] = {
    'isSignal' : 0,
    'isData'   : 0
    }

structure['Vg'] = {
    'isSignal' : 0,
    'isData'   : 0
    }

structure['VVV'] = {
    'isSignal' : 0,
    'isData'   : 0
    }

structure['ZZ'] = {
    'isSignal' : 0,
    'isData'   : 0
    }

structure['WZ'] = {
    'isSignal' : 0,
    'isData'   : 0
    }

structure['VgS'] = {
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




#######################

structure['WW'] = {
    'isSignal' : 1,
    'isData'   : 0
    }

#######################


structure['Fake']  = {
    'isSignal' : 0,
    'isData'   : 0
    }

structure['DATA']  = {
    'isSignal' : 0,
    'isData'   : 1
    }


for nuis in nuisances.values():
    if 'cutspost' in nuis:
        print(nuis)
        nuis['cuts'] = nuis['cutspost']
        print(nuis)



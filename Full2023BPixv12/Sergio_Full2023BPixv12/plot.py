groupPlot = {}

groupPlot['DY']  = {  
    'nameHR'   : 'DY',
    'isSignal' : 0,
    'color'    : 418, #kGreen+4
    'samples'  : ['DY']
}

groupPlot['top']  = {
    'nameHR'   : 'Top',
    'isSignal' : 0,
    'color'    : 400,
    'samples'  : ['top']
}

groupPlot['WZ']  = {
    'nameHR'   : 'WZ',
    'isSignal' : 0,
    'color'    : 619,
    'samples'  : ['WZ']
}

groupPlot['ZZ']  = {
    'nameHR'   : 'ZZ',
    'isSignal' : 0,
    'color'    : 617,
    'samples'  : ['ZZ']
}

groupPlot['Fake']  = {
    'nameHR' : 'nonprompt',
    'isSignal' : 0,
    'color': 921,    # kGray + 1
    'colorPlt': "#778899",
    'samples'  : ['Fake']
}

groupPlot['WW']  = {
    'nameHR'   : 'WW',
    'isSignal' : 0,
    'color'    : 851,
    'samples'  : ['WW','ggWW']
}

groupPlot['VVV']  = {  
    'nameHR' : 'VVV',
    'isSignal' : 0,
    'color': 857, # kAzure -3
    'colorPlt': "#4b0082",
    'samples'  : ['VVV']
}

groupPlot['Vg']  = {  
    'nameHR' : "$V\gamma$",
    'isSignal' : 0,
    'color'    : 810,   # kOrange + 10
    'colorPlt': "#e76300",
    'samples'  : ['Vg', 'VgS']
}

groupPlot['ggF']  = {
    'nameHR' : "ggF",
    'isSignal' : 1,
    'color'    : 623,
    'colorPlt': "",
    'samples'  : ['ggH_hww']
}

groupPlot['VBF']  = {
    'nameHR' : "VBF",
    'isSignal' : 1,
    'color'    : 600,
    'colorPlt': "",
    'samples'  : ['qqH_hww']
}

plot = {}


plot['DY']  = {  
    'color'    : 418,    # kGreen+2
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['Fake']  = {
    'color': 921,    # kGray + 1
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0
}

plot['top']  = {
    'color'    : 400,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['WW']  = {
    'color'    : 851,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['ggWW']  = {
    'color'    : 851,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['Vg']  = { 
    'color': 859,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0
}

plot['VgS']  = { 
    'color'    : 859, # kAzure -1  
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0
}

plot['WZ']  = {
    'color'    : 619,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['ZZ']  = {
    'color'    : 617,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['VVV']  = { 
    'color': 857, # kAzure -3  
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0
}

plot['qqH_hww'] = {
    'nameHR' : 'qqH',
    'color': 632+1, # kRed+1 
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : 1    #
}

plot['ggH_hww'] = {
    'nameHR' : 'ggH',
    'color': 632, # kRed 
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : 1    #
}

# data

plot['DATA']  = { 
    'nameHR'   : 'Data',
    'color'    : 1 ,  
    'isSignal' : 0,
    'isData'   : 1 ,
    'isBlind'  : 0
}


# Legend definition
legend = {}
legend['lumi'] = 'L = 9.45 fb^{-1}'
legend['sqrt'] = '#sqrt{s} = 13.6 TeV'

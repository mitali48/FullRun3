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
    'samples'  : ['Top']
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
    'samples'  : ['Fake_e', 'Fake_m']
}

groupPlot['WW']  = {
    'nameHR' : 'WW',
    'isSignal' : 0,
    'color': 851, # kAzure -9 
    'colorPlt': "#87cefa",
    'samples': [f'{sample}_B{i}' for sample in ('WW', 'ggWW') for i in range(nbins)]
}


groupPlot['WW_nonfid']  = {
    'nameHR' : 'WW nonfid',
    'isSignal' : 0,
    'color': 853, # kAzure -9 
    'colorPlt': "#009dff",
    'samples'  : ['WW_nonfid', 'ggWW_nonfid']
}

groupPlot['VVV']  = {  
    'nameHR' : 'VVV',
    'isSignal' : 0,
    'color': 857, # kAzure -3
    'colorPlt': "#4b0082",
    'samples'  : ['VVV']
}


groupPlot['Vg']  = {  
   'nameHR' : "$V\\gamma$",
   'isSignal' : 0,
   'color'    : 810,   # kOrange + 10
   'colorPlt': "#e76300",
   'samples'  : ['Vg', 'VgS']
#    'samples'  : ['Zg', 'Wg', 'ZgS', 'WgS']
}

# groupPlot['Higgs']  = {
#     'nameHR' : "Higgs",
#     'isSignal' : 0,
#     'color'    : 623,
#     'colorPlt': "",
#     'samples'  : ['Higgs']
# }

plot = {}


plot['DY']  = {  
    'color'    : 418,    # kGreen+2
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['Fake_e']  = {
    'color': 921,    # kGray + 1
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0
}

plot['Fake_m']  = { 
    'color': 921,    # kGray + 1
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0
}

plot['Top']  = {
    'color'    : 400,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

for i in range(nbins):
    plot[f'WW_B{i}'] = {
        'color': 851, # kAzure -9 
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0  
    }

    plot[f'ggWW_B{i}'] = {
        'color': 851, # kAzure -9 
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0   
    }

plot['WW_nonfid'] = {
    'color': 853, # kAzure -9 
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0   
    }

plot['ggWW_nonfid'] = {
    'color': 853, # kAzure -9 
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0   
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

# plot['Higgs'] = {
#     'nameHR' : 'Higgs',
#     'color': 632+1, # kRed+1 
#     'isSignal' : 0,
#     'isData'   : 0,    
#     'scale'    : 1    #
# }

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
legend['lumi'] = 'L = 109.0 fb^{-1}'
legend['sqrt'] = '#sqrt{s} = 13.6 TeV'

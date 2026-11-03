# 1. Flatten the cuts dictionary into a list (cuts2j)
_mergedCuts = []
for cut in list(cuts.keys()):
    if type(cuts[cut]) == dict:
        for cat in list(cuts[cut]['categories'].keys()):
            _mergedCuts.append(cut + '_' + cat)
    elif type(cuts[cut]) == str:
        _mergedCuts.append(cut)

cuts2j = _mergedCuts

# 2. Define your variables and apply blinding to SR
variables = {}

variables['events'] = {
    'name'  : '1',      
    'range' : (1,0,1),  
    'xaxis' : 'events', 
    'fold'  : 3,
    # This will match SR_0j, SR_1j, and SR_maj2j and set them to 'full' blinding
    'blind' : dict([(cut, 'full') for cut in cuts2j if cut.startswith('SR')])
}

# mll binning: Exactly 4.0 GeV per bin (300 / 75 = 4) -> (75 bins, 85, 385)
# mll binning for DY: Exactly 5.0 GeV per bin (50 / 10 = 5) -> (10 bins, 35, 85)

variables['mll'] = {
    'name': 'mll',    
    'range' : (74, 85, 385), 
    'xaxis' : 'm_{ll} [GeV]',
    'fold' : 0,
    'blind' : dict([(cut, 'full') for cut in cuts2j if cut.startswith('SR')])
}

variables['ptll']  = {  
    'name': 'ptll',     
    'range' : (40, 0,200),   
    'xaxis' : 'p_{T}^{ll} [GeV]',
    'fold' : 0,
    'blind' : dict([(cut, 'full') for cut in cuts2j if cut.startswith('SR')])
}

variables['pt1']  = { 
    'name': 'Lepton_pt[0]',     
    'range' : (40,0,200),
    'xaxis' : 'p_{T} 1st lep',
    'fold'  : 3,  
    'blind' : dict([(cut, 'full') for cut in cuts2j if cut.startswith('SR')])                    
}

variables['pt2']  = {
    'name': 'Lepton_pt[1]',     
    'range' : (40,0,200),   
    'xaxis' : 'p_{T} 2nd lep',
    'fold'  : 3,
    'blind' : dict([(cut, 'full') for cut in cuts2j if cut.startswith('SR')])                       
}

variables['eta1']  = {
    'name': 'Lepton_eta[0]',     
    'range' : (40,-3,3),   
    'xaxis' : '#eta 1st lep',
    'fold'  : 3,  
    'blind' : dict([(cut, 'full') for cut in cuts2j if cut.startswith('SR')])                    
}

variables['eta2']  = {
    'name': 'Lepton_eta[1]',     
    'range' : (40,-3,3),   
    'xaxis' : '#eta 2nd lep',
    'fold'  : 3,    
    'blind' : dict([(cut, 'full') for cut in cuts2j if cut.startswith('SR')])                    
}

variables['puppimet']  = {
    'name': 'PuppiMET_pt',
    'range' : (20,0,200),
    'xaxis' : 'Puppi MET p_{T} [GeV]',
    'fold' : 3,
    'blind' : dict([(cut, 'full') for cut in cuts2j if cut.startswith('SR')])
}

### Jets
variables['njet']  = {
    'name': 'Sum(CleanJet_pt>30)',
    'range' : (5,0,5),
    'xaxis' : 'Number of jets',
    'fold' : 2,
    'blind' : dict([(cut, 'full') for cut in cuts2j if cut.startswith('SR')])
}

variables['jetpt1']  = {
    #'name': 'Alt(CleanJet_pt, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
    'name': 'Alt(CleanJet_pt, 0, -99)',
    'range' : (40,0,200),
    'xaxis' : 'p_{T} 1st jet',
    'fold' : 0,
    'blind' : dict([(cut, 'full') for cut in cuts2j if cut.startswith('SR')])
}

variables['jetpt2']  = {
    #'name': 'Alt(CleanJet_pt, 1, -99)  - 9999.9*(CleanJet_pt[1]<30)',
    'name': 'Alt(CleanJet_pt, 1, -99)',
    'range' : (40,0,200),
    'xaxis' : 'p_{T} 2nd jet',
    'fold' : 0,
    'blind' : dict([(cut, 'full') for cut in cuts2j if cut.startswith('SR')])
}

variables['jeteta1']  = {
    #'name': 'Alt(CleanJet_eta, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
    'name': 'Alt(CleanJet_eta, 0, -99)',
    'range' : (30,-4.7,4.7),
    'xaxis' : '#eta 1st jet',
    'fold' : 0,
    'blind' : dict([(cut, 'full') for cut in cuts2j if cut.startswith('SR')])
}

variables['jeteta2']  = {
    #'name': 'Alt(CleanJet_eta, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
    'name': 'Alt(CleanJet_eta, 1, -99)',
    'range' : (30,-4.7,4.7),
    'xaxis' : '#eta 2nd jet',
    'fold' : 0,
    'blind' : dict([(cut, 'full') for cut in cuts2j if cut.startswith('SR')])
}

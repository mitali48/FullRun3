cuts = {}

_tmp = [
    'Lepton_pt[0] > 25.', #reduce misidentified leptons
    'Lepton_pt[1] > 20.', 
    '(nLepton >= 2 && Alt(Lepton_pt,2, 0) < 10.)', #to suppress backgrounds from WZ and ZZ processes
    # 'abs(Lepton_eta[0]) < 2.5',
    # 'abs(Lepton_eta[1]) < 2.5',
    'noJetInHorn'
]

preselections = ' && '.join(_tmp)

cuts['Top_CR_emu']  = {
    'expr' : 'Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'categories' : {
        '0j' : 'zeroJet',
        '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
        '2j' : 'Sum(CleanJet_pt>30.0)==2',
        'Inc' : '1',
    }
}

cuts['Top_CR_mll85_emu']  = {
    'expr' : 'mll>85 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'categories' : {
        '0j' : 'zeroJet',
        '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
        '2j' : 'Sum(CleanJet_pt>30.0)==2',
        'Inc' : '1',
    }
}

cuts['Top_CR']  = {
    'expr' : 'topcr',
    'categories' : {
        '0j' : 'zeroJet',
        '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
        '2j' : 'Sum(CleanJet_pt>30.0)==2',
        'Inc' : '1',
    }
}
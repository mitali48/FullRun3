cuts = {}

_tmp = [
    'Lepton_pt[0] > 25.', #reduce misidentified leptons
    'Lepton_pt[1] > 20.', 
    '(nLepton >= 2 && Alt(Lepton_pt,2, 0) < 10.)', #to suppress backgrounds from WZ and ZZ processes
    'noJetInHorn'
]

preselections = ' && '.join(_tmp)

cuts['SR'] = {
    'expr': 'mll > 85 && bVeto && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'categories' : {
        '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0 ',
        '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0 ',
        '2j' : 'Sum(CleanJet_pt>30.0)==2',
        '3j' : 'Sum(CleanJet_pt>30.0)>=3',
        'Inc': 'mll > 12',
    }
}
cuts['Top_CR']  = {
    'expr' : 'mll > 85 && ( ((zeroJet && !bVeto) || bReq1)  || bReq2 ) && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'categories' : {
        '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0',
        '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0',
        '2j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)>30.0 && Alt(CleanJet_pt,2, 0.0)<30.0',
        '3j' : 'Sum(CleanJet_pt>30.0)>=3',
        'Inc' : 'mll > 12',
    }
}

cuts['DYtautauCR']  = {
   'expr' : 'ptll < 30 && mll < 85 && bVeto && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
   'categories' : {
       '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0',
       '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0',
       '2j' : 'Sum(CleanJet_pt>30.0)==2',
       '3j' : 'Sum(CleanJet_pt>30.0)>=3',
       'Inc': 'mll > 12',
   }
}

cuts['nonpromptCR'] = {
    'expr': 'bVeto && mll>85 && Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13',
    'categories' : {
        '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0',
        '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0',
        '2j' : 'Sum(CleanJet_pt>30.0)==2',
        '3j' : 'Sum(CleanJet_pt>30.0)>=3',
        'Inc': 'mll > 12',
    }
}
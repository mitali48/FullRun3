cuts = {}

_tmp = [
    #'Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'Lepton_pt[0] > 25.', #reduce misidentified leptons
    'Lepton_pt[1] > 20.', 
    '(abs(Lepton_pdgId[1]) == 13 || Lepton_pt[1] > 13.)',
    '(nLepton >= 2 && Alt(Lepton_pt,2, 0) < 10.)', #to suppress backgrounds from WZ and ZZ processes
    # 'Sum(CleanJet_pt > 30 && abs(CleanJet_eta) >= 2.5) == 0'
    # 'Sum(abs(CleanJet_eta) >= 2.5) == 0', #adapted from Run3 WW analysis as looking at jets outside tracker acceptance does not make sense for this analysis
    #'ptll>15',
    #'mll > 12',
    # '(zeroJet || Sum(CleanJet_pt>30.0)<=3)', #suppress QCD background 
    # 'allJetsInHorn_atLeastOne'
    #'anyJetInHorn' 
    # 'noJetInHorn_pT30'
    #'noJetInHorn_pT15'
    #'noJetInHorn'
]

preselections = ' && '.join(_tmp)

'''
cuts['Check'] = {
    'expr' : '1,'
    'categories' : {
        'Inc' : '1'
    }
}

cuts['Zee']  = {
   'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*11) && mll > 60 && mll < 120',
   'categories' : {
       '0j' : 'zeroJet',
       '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
       '2j' : 'multiJet',
       'Inc' : '1',
  }
}

cuts['Zmm']  = {
    'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -13*13) && mll > 60 && mll < 120',
    'categories' : {
        '0j' : 'zeroJet',
        '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
        '2j' : 'multiJet',
        'Inc' : '1',
    }
}

cuts['ww2l2v_hww'] = {
    'expr': 'sr && mpmet>15 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'categories' : {
        '0j_pt2gt20' : 'Alt(CleanJet_pt,0, 0.0)<30.0 && Lepton_pt[1]>=20',
        '0j_pt2lt20' : 'Alt(CleanJet_pt,0, 0.0)<30.0 && Lepton_pt[1]<20',
        '1j_pt2gt20' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0 && Lepton_pt[1]>=20',
        '1j_pt2lt20' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0 && Lepton_pt[1]<20',
        '2j' : 'Sum(CleanJet_pt>30.0)==2',
        'Inc': 'mll>12',
    }
}


cuts['ww2l2v_ss'] = {
    'expr': 'bVeto && mll>85  && Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13',
    'categories' : {
        'Inc': '1',
        '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0',
        '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0',
        '2j' : 'Sum(CleanJet_pt>30.0)==2',
    }
}

'''

cuts['ww2l2v_sr']  = {
   'expr' : 'sr',
   'categories' : { 
       '0j' : 'zeroJet',
       '1j' : 'oneJet',
       '2j' : 'twoJet',
       '3j' : 'multiJet',
       'Inc': '1',
   }
}

cuts['ww2l2v_top']  = { 
   'expr' : 'topcr ',
   'categories' : { 
       '0j' : 'zeroJet',
       '1j' : 'oneJet',
       '2j' : 'twoJet',
       '3j' : 'multiJet',
       'Inc': '1',
   }
}

cuts['ww2l2v_dytt']  = { 
   'expr' : 'dycr ',
   'categories' : { 
       '0j' : 'zeroJet',
       '1j' : 'oneJet',
       '2j' : 'twoJet',
       '3j' : 'multiJet',
       'Inc': '1',
   }
}
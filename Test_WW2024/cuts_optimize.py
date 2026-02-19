cuts = {}

_tmp = [
    'Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    # 'Lepton_pt[0] > 25.',
    # 'Lepton_pt[1] > 20.', 
    '(abs(Lepton_pdgId[1]) == 13 || Lepton_pt[1] > 13.)',
    '(nLepton >= 2 && Alt(Lepton_pt,2, 0) < 10.)',
    #'ptll>15',
    #'mll > 12',
    '(zeroJet || Sum(CleanJet_pt>30.0)<=3)',
    # 'allJetsInHorn_atLeastOne'
    #'anyJetInHorn' 
    # 'noJetInHorn_pT30'
    #'noJetInHorn_pT15'
    # 'noJetInHorn'
]

preselections = ' && '.join(_tmp)


cuts['sr_pt1-25-pt2-15']  = {
   'expr' : 'bVeto && Lepton_pt[0] > 25. && Lepton_pt[1] > 15.',
   'categories' : {
       '0j' : 'zeroJet',
       '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
       '2j' : 'multiJet',
       'Inc' : '1',
  }
}


cuts['sr_pt1-25-pt2-18']  = {
   'expr' : 'bVeto && Lepton_pt[0] > 25. && Lepton_pt[1] > 18.',
   'categories' : {
       '0j' : 'zeroJet',
       '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
       '2j' : 'multiJet',
       'Inc' : '1',
  }
}


cuts['sr_pt1-25-pt2-20']  = {
   'expr' : 'bVeto && Lepton_pt[0] > 25. && Lepton_pt[1] > 20.',
   'categories' : {
       '0j' : 'zeroJet',
       '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
       '2j' : 'multiJet',
       'Inc' : '1',
  }
}


cuts['sr_pt1-25-pt2-25']  = {
   'expr' : 'bVeto && Lepton_pt[0] > 25. && Lepton_pt[1] > 25.',
   'categories' : {
       '0j' : 'zeroJet',
       '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
       '2j' : 'multiJet',
       'Inc' : '1',
  }
}
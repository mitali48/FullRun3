cuts = {}

_tmp = [
    #'Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'Lepton_pt[0] > 25.',
    'Lepton_pt[1] > 10.',
    '(abs(Lepton_pdgId[1]) == 13 || Lepton_pt[1] > 13.)',
    '(nLepton >= 2 && Alt(Lepton_pt,2, 0) < 10.)',
    'ptll>15',
    'mll > 12',
    '(zeroJet || Sum(CleanJet_pt>30.0)<=3)',
    'noJetInHorn'
]

preselections = ' && '.join(_tmp)

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

cuts['hww2l2v_13TeV_ss'] = {
    'expr': 'bVeto && mll>35 && mpmet<30 && Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13',
    'categories' : {
        'Inc': 'mll>12',
        '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0',
        '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0',
        '2j' : 'Sum(CleanJet_pt>30.0)==2',
    }
}

cuts['hww2l2v_13TeV_sr'] = {
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

cuts['hww2l2v_13TeV_ww']  = {
   'expr' : 'wwcr && mpmet>15 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
   'categories' : {
       '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0',
       '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0',
       '2j' : 'Sum(CleanJet_pt>30.0)==2',
       'Inc': 'mll>12',
   }
}

cuts['hww2l2v_13TeV_top']  = { 
   'expr' : 'topcr && mpmet>15 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
   'categories' : {
       '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0',
       '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0',
       '2j' : 'Sum(CleanJet_pt>30.0)==2',
       'Inc': 'mll>12',
   }
}

cuts['hww2l2v_13TeV_dytt']  = { 
   'expr' : 'dycr && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
   'categories' : { 
       '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0',
       '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0',
       '2j' : 'Sum(CleanJet_pt>30.0)==2',
       'Inc': 'mll>12',
   }
}

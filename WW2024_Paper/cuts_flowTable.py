cuts = {}

preselections = 'Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13'

# cuts['lep_pt1_25']  = { 
#     'expr' : 'Lepton_pt[0] > 25.',
#     'categories' : {
#        '0j' : 'zeroJet',
#        '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
#        '2j' : 'multiJet',
#        'Inc' : '1',
#   }
# }

# cuts['lep_pt2_20']  = {
#     'expr' : 'Lepton_pt[0] > 25. && Lepton_pt[1] > 20.',
#     'categories' : {
#        '0j' : 'zeroJet',
#        '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
#        '2j' : 'multiJet',
#        'Inc' : '1',
#   }
# }

cuts['lepton_pT_e-mu']  = {
    'expr' : 'Lepton_pt[0] > 25. && Lepton_pt[1] > 20. ',
    'categories' : {
       '0j' : 'zeroJet',
       '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
       '2j' : 'multiJet',
       'Inc' : '1',
    }
}

cuts['veto_third_lepton']  = {
    'expr' : 'Lepton_pt[0] > 25. && Lepton_pt[1] > 20. && (nLepton >= 2 && Alt(Lepton_pt,2, 0) < 10.)',
    'categories' : {
       '0j' : 'zeroJet',
       '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
       '2j' : 'multiJet',
       'Inc' : '1',
    }
}

cuts['preSel_mll_85']  = {
    'expr' : 'preSel && mll>85',
    'categories' : {
       '0j' : 'zeroJet',
       '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
       '2j' : 'multiJet',
       'Inc' : '1',
    }
}

cuts['top_mll_85_bReq_atleast1']  = {
    'expr' : 'preSel && mll>85 && ((zeroJet && !bVeto) || bReq)',
    'categories' : {
       '0j' : 'zeroJet',
       '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
       '2j' : 'multiJet',
       'Inc' : '1',
    }
}

cuts['top_mll_85_bReq1_bReq2']  = {
    'expr' : 'preSel && mll>85 && ( ((zeroJet && !bVeto) || bReq1)  || bReq2 )',
    'categories' : {
       '0j' : 'zeroJet',
       '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
       '2j' : 'multiJet',
       'Inc' : '1',
    }
}

# cuts['sr_mll_85']  = {
#    'expr' : 'preSel && mll>85',
#    'categories' : {
#        '0j' : 'zeroJet',
#        '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
#        '2j' : 'multiJet',
#        'Inc' : '1',
#     }
# }

cuts['sr_mll_85_bVeto']  = {
   'expr' : 'preSel && mll>85 && bVeto',
   'categories' : {
       '0j' : 'zeroJet',
       '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
       '2j' : 'multiJet',
       'Inc' : '1',
    }
}

cuts['dytt_mll_85']  = {
    'expr' : 'preSel && mll<85',
    'categories' : {
       '0j' : 'zeroJet',
       '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
       '2j' : 'multiJet',
       'Inc' : '1',
    }
}

cuts['dytt_mll_85_ptll_30']  = {
    'expr' : 'preSel && mll<85 && ptll<30',
    'categories' : {
       '0j' : 'zeroJet',
       '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
       '2j' : 'multiJet',
       'Inc' : '1',
    }
}

cuts['dytt_mll_85_ptll_30_bVeto']  = {
    'expr' : 'preSel && mll<85 && ptll<30 && bVeto',
    'categories' : {
       '0j' : 'zeroJet',
       '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
       '2j' : 'multiJet',
       'Inc' : '1',
    }
}


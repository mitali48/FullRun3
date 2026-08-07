cuts = {}

_tmp = [
    'Lepton_pt[0] > 25.', #reduce misidentified leptons
    'Lepton_pt[1] > 20.', 
    '(nLepton >= 2 && Alt(Lepton_pt,2, 0) < 10.)', #to suppress backgrounds from WZ and ZZ processes
    'noJetInHorn'
]

preselections = ' && '.join(_tmp)

# Gen level jet categorization
catGenLevel = { 
    'B0'  : '1'
    # 'B0' : 'nCleanGenJets == 0',
    # 'B1' : 'nCleanGenJets == 1',
    # 'B2' : 'nCleanGenJets == 2',
    # 'B3' : 'nCleanGenJets >= 3',
}
# Reco level jet categorization
catRecoLevel = {
    '0j' : 'zeroJet',
    '1j' : 'oneJet',
    '2j' : 'twoJet',
    '3j' : 'multiJet',
}

cuts['SR'] = {
    'expr': 'sr',
    'categories': catRecoLevel
}


cuts['OnebTag_CR']  = {
    'expr' : 'Onebtagcr',
    'categories' :  catRecoLevel
}

cuts['TwobTag_CR']  = {
    'expr' : 'Twobtagcr',
    'categories' :  catRecoLevel
}

cuts['Top_CR']  = {
    'expr' : 'topcr',
    'categories' :  catRecoLevel
}

cuts['DYtautau_CR']  = {
   'expr' : 'dycr',
   'categories' : catRecoLevel 
}

cuts['ss_CR'] = {
    'expr': 'nonpromptcr',
    'categories' : catRecoLevel 
}

# cuts['SR'] = {
#     'expr': 'sr',
#     'categories': dict(
#         (iReco + '_' + iGen,
#          catRecoLevel[iReco] + ' && ' + catGenLevel[iGen])
#         for iReco in catRecoLevel
#         for iGen in catGenLevel
#     )
# }

# The above code creates a dictionary of cuts for the signal region (SR) based on both reconstructed (Reco) and generated (Gen) jet categories. 
# Each category is defined by a combination of Reco and Gen jet conditions, allowing for detailed analysis of events based on their jet multiplicity at both levels.

# {
#     '0j_B0': 'zeroJet && nCleanGenJets == 0',
#     '0j_B1': 'zeroJet && nCleanGenJets == 1',
#     '0j_B2': 'zeroJet && nCleanGenJets == 2',
#     '0j_B3': 'zeroJet && nCleanGenJets >= 3',

#     '1j_B0': 'oneJet && nCleanGenJets == 0',
#     '1j_B1': 'oneJet && nCleanGenJets == 1',
#     '1j_B2': 'oneJet && nCleanGenJets == 2',
#     '1j_B3': 'oneJet && nCleanGenJets >= 3',

#     '2j_B0': 'twoJet && nCleanGenJets  == 0',
#     '2j_B1': 'twoJet && nCleanGenJets == 1',
#     '2j_B2': 'twoJet && nCleanGenJets == 2',
#     '2j_B3': 'twoJet && nCleanGenJets >= 3',

#     '3j_B0': 'multiJet && nCleanGenJets == 0',
#     '3j_B1': 'multiJet && nCleanGenJets == 1',
#     '3j_B2': 'multiJet && nCleanGenJets == 2',
#     '3j_B3': 'multiJet && nCleanGenJets >= 3',
# }


# cuts['DYmumuCR']  = {
#    'expr' : 'mll > 60 && mll < 120 && bVeto && Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13',
#    'categories' : {
#        '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0',
#        '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0',
#        '2j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)>30.0 && Alt(CleanJet_pt,2, 0.0)<30.0',
#        '3j' : 'Sum(CleanJet_pt>30.0)>=3',
#        'Inc': 'mll > 12',
#    }
# }

# cuts['DYeeCR']  = {
#    'expr' : 'mll > 60 && mll < 120 && bVeto && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11',
#    'categories' : {
#        '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0',
#        '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0',
#        '2j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)>30.0 && Alt(CleanJet_pt,2, 0.0)<30.0',
#        '3j' : 'Sum(CleanJet_pt>30.0)>=3',
#        'Inc': 'mll > 12',
#    }
# }
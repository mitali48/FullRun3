structure= {}

for i in range(nbins):

    structure[f'WW_B{i}'] = {
        'isSignal': 1,
        'isData': 0,
    }

    structure[f'ggWW_B{i}'] = {
        'isSignal': 1,
        'isData': 0,
    }

    
structure['WW_nonfid'] = {
    'isSignal': 1,
    'isData': 0,
}

structure['ggWW_nonfid'] = {
    'isSignal': 1,
    'isData': 0,
}

# structure['WW'] = {
#     'isSignal': 1,
#     'isData': 0,
# }

# structure['ggWW'] = {
#     'isSignal': 1,
#     'isData': 0,
# }

backgrounds = [
    'DY',
    'Top',
    'WZ',
    'ZZ',
    'Vg',
    'VgS',
    'VVV',
    'Fake_e',
    'Fake_m'
]

# 'Higgs',

for sample in backgrounds:
    structure[sample] = {
        'isSignal': 0,
        'isData': 0,
    }


structure['DATA'] = {
    'isSignal': 0,
    'isData': 1,
}


for nuis in nuisances.values():
    if 'cutspost' in nuis:
        print(nuis)
        nuis['cuts'] = nuis['cutspost']
        print(nuis)
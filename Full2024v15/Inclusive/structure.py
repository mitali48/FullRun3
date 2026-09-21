structure= {}

signals = [
    'WW',
    'ggWW',
]

for sample in signals:
    structure[sample] = {
        'isSignal': 1,
        'isData': 0,
    }


backgrounds = [
    'DY',
    'Top',
    'WZ',
    'ZZ',
    'Vg',
    'VgS',
    'VVV',
    'Higgs',
    'Fake_e',
    'Fake_m'
]

for sample in backgrounds:
    structure[sample] = {
        'isSignal': 0,
        'isData': 0,
    }


structure['DATA'] = {
    'isSignal': 0,
    'isData': 1,
}
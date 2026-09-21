# ============================================================
# Structure for mkDatacards
# ============================================================

structure = {}

# ------------------------------------------------------------
# Signal: WW / ggWW fiducial B categories
# ------------------------------------------------------------

for i in range(4):

    structure[f'WW_B{i}'] = {
        'isSignal': 1,
        'isData': 0,
    }

    structure[f'ggWW_B{i}'] = {
        'isSignal': 1,
        'isData': 0,
    }


# ------------------------------------------------------------
# Non-fiducial WW / ggWW
# ------------------------------------------------------------

structure['WW_nonfid'] = {
    'isSignal': 1,
    'isData': 0,
}

structure['ggWW_nonfid'] = {
    'isSignal': 1,
    'isData': 0,
}


# ------------------------------------------------------------
# Backgrounds
# ------------------------------------------------------------

backgrounds = [
    'DY',
    'Top',
    'WZ',
    'ZZ',
    'Vg',
    'VgS',
    'VVV',
    'ggH_hww',
    'qqH_hww',
    'Fake',
]

for sample in backgrounds:
    structure[sample] = {
        'isSignal': 0,
        'isData': 0,
    }


# ------------------------------------------------------------
# Data
# ------------------------------------------------------------

structure['DATA'] = {
    'isSignal': 0,
    'isData': 1,
}
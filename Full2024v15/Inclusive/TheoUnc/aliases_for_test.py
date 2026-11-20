import os
import copy
import inspect
import ROOT
import json
from collections import OrderedDict

ROOT.gSystem.Load("libGpad.so")
ROOT.gSystem.Load("libGraf.so")
ROOT.gSystem.Load("libc.so")

macros = '/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/utils/macros/'
fakerates = '/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/utils/data/FakeRate/'
btagmaps = '/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/utils/data/btag/'
extended='/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/extended/'
theosys= '/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/utils/data/TheoUnc/2024/'

if __name__ == "__main__":
    print(macros)
    print(fakerates)
    print(btagmaps)
    print(extended)
    print(theosys)

aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA')]

with open(theosys + 'NormTHU_2024_Inclusive.json', 'r') as f:
    NormTHU = json.load(f)

for sample in NormTHU.keys():

    for varName, norm in NormTHU[sample].items():

        # --- 1. Single float variations (Envelope nuisances) ---
        if isinstance(norm, (int, float)):

            val = norm

            if abs(val) > 10 or abs(val) < 0.1:
                val = 1.
                NormTHU[sample][varName] = 1.
                print(f"[WARNING] {varName} nuisance variation is faulty, set to 1.0")

            alias_name = f'NormTHU_{sample}_{varName}'

            aliases[alias_name] = {
                'expr': str(val),
                'samples': sample
            }

            print(f"{alias_name} = {val}")


        # --- 2. Dictionary variations (Up/Down) ---
        elif isinstance(norm, dict):

            val_up = norm['Up']
            val_down = norm['Down']

            if abs(val_up) > 10 or abs(val_up) < 0.1:
                val_up = 1.
                print(f"[WARNING] {varName} Up variation is faulty, set to 1.0")

            if abs(val_down) > 10 or abs(val_down) < 0.1:
                val_down = 1.
                print(f"[WARNING] {varName} Down variation is faulty, set to 1.0")

            NormTHU[sample][varName]['Up'] = val_up
            NormTHU[sample][varName]['Down'] = val_down

            if 'pdf' not in varName.lower():

                alias_up = f'NormTHU_{sample}_{varName}_Up'
                alias_down = f'NormTHU_{sample}_{varName}_Down'

                aliases[alias_up] = {
                    'expr': str(val_up),
                    'samples': sample
                }

                aliases[alias_down] = {
                    'expr': str(val_down),
                    'samples': sample
                }

                print(f"{alias_up} = {val_up}")
                print(f"{alias_down} = {val_down}")

            else:

                alias_name = f'NormTHU_{sample}_{varName}'

                aliases[alias_name] = {
                    'expr': str(val_up),
                    'samples': sample
                }

                print(f"{alias_name} = {val_up}")


        # --- 3. Two-element list variations (Up/Down) ---
        elif isinstance(norm, list) and len(norm) == 2:

            val_up = norm[0]
            val_down = norm[1]

            if abs(val_up) > 10 or abs(val_up) < 0.1:
                val_up = 1.
                print(f"[WARNING] {varName} Up variation is faulty, set to 1.0")

            if abs(val_down) > 10 or abs(val_down) < 0.1:
                val_down = 1.
                print(f"[WARNING] {varName} Down variation is faulty, set to 1.0")

            NormTHU[sample][varName] = [val_up, val_down]

            if 'pdf' not in varName.lower():

                alias_up = f'NormTHU_{sample}_{varName}_Up'
                alias_down = f'NormTHU_{sample}_{varName}_Down'

                aliases[alias_up] = {
                    'expr': str(val_up),
                    'samples': sample
                }

                aliases[alias_down] = {
                    'expr': str(val_down),
                    'samples': sample
                }

                print(f"{alias_up} = {val_up}")
                print(f"{alias_down} = {val_down}")

            else:

                alias_name = f'NormTHU_{sample}_{varName}'

                aliases[alias_name] = {
                    'expr': str(val_up),
                    'samples': sample
                }

                print(f"{alias_name} = {val_up}")


# LepSF2l__ele_cutBased_MediumID_tthMVA_Run3__mu_cut_TightID_pfIsoLoose_HWW_tthmva_67
eleWP = 'cutBased_MediumID_tthMVA_Run3'
muWP  = 'cut_TightID_pfIsoLoose_HWW_tthmva_67'

aliases['LepWPCut'] = {
    'expr': 'LepCut2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc + ['DATA'],
}
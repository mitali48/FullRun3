import ROOT
import os
import re
import json
from optparse import OptionParser

parser = OptionParser()

parser.add_option(
    "-f", "--inputFile",
    dest="ifile",
    default="input.root",
    type="string",
    help="ROOT input file"
)
parser.add_option(
    "-c", "--category",
    dest="category",
    default="All_incl",
    type="string",
    help="ROOT input category"
)

parser.add_option(
    "-v", "--variable",
    dest="variable",
    default="events",
    type="string",
    help="ROOT input variable"
)

parser.add_option(
    "-y", "--year",
    dest="year",
    default="2024",
    type="string",
    help="Year of the analysis"
)

parser.add_option(
    "-t", "--config",
    dest="config",
    default="Inclusive",
    type="string",
    help="Configuration type: inclusive or njets or other specific configuration"
)

parser.add_option(
    "-o", "--outputDir",
    dest="outputDir",
    default="/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/utils/data/TheoUnc",
    type="string",
    help="Output directory for JSON file"
)

(options, args) = parser.parse_args()

ifile = options.ifile
category = options.category
variable = options.variable
year = options.year
config = options.config
outputDir = options.outputDir


# Samples to process
samples = ['WW', 'ggWW']


# Open ROOT file
rfile = ROOT.TFile.Open(ifile)

if not rfile or rfile.IsZombie():
    raise RuntimeError(f"Could not open ROOT file: {ifile}")


# Get category/variable directory
rdir = rfile.Get(f"{category}/{variable}")

if not rdir:
    raise RuntimeError(f"Directory {category}/{variable} not found in {ifile}")

keys = rdir.GetListOfKeys()


# Store normalization factors
norm = {}

# Store nominal integrals
nominal = {}


# --------------------------------------------------
# 1. Get nominal integrals
# --------------------------------------------------

for sample in samples:

    histo = rfile.Get(
        f"{category}/{variable}/histo_{sample}"
    )

    if not histo:
        print(f"WARNING: Nominal histogram missing for {sample}")
        continue

    nominal[sample] = histo.Integral()

    norm[sample] = {}

    print("\n--------------------------------------")
    print(f"Sample: {sample}")
    print(f"Nominal integral = {nominal[sample]}")
    print("--------------------------------------")


# --------------------------------------------------
# 2. Process systematic variations
# --------------------------------------------------

for key in keys:

    key_name = key.GetName()

    # Identify sample
    matched_sample = None

    for sample in samples:

        if key_name.startswith(f"histo_{sample}_"):
            matched_sample = sample
            break

    if not matched_sample:
        continue

    # Skip samples without nominal histograms
    if matched_sample not in nominal:
        continue

    histo = rfile.Get(
        f"{category}/{variable}/{key_name}"
    )

    if not histo:
        continue

    integral = histo.Integral()

    print(f"\n{key_name}: integral = {integral}")


    # ----------------------------------------------
    # SPECIAL_NUIS envelope variations
    # ----------------------------------------------

    envelope_match = re.search(
        r'^histo_' + re.escape(matched_sample) +
        r'_(.*_SPECIAL_NUIS_envelope\d+)$',
        key_name
    )

    if envelope_match:

        var = envelope_match.group(1)

        norm_factor = (
            nominal[matched_sample] / integral
            if integral != 0 else 0.
        )

        norm[matched_sample][var] = norm_factor

        print(f"  Variation : {var}")
        print(f"  Norm      : {norm_factor}")

        continue


    # ----------------------------------------------
    # Standard Up/Down variations
    # ----------------------------------------------

    prefix = f"histo_{matched_sample}_"

    variation_name = key_name.replace(prefix, "", 1)

    match = re.match(r'^(.*?)(Up|Down)$', variation_name)

    if not match:
        continue

    var = match.group(1)
    direction = match.group(2)

    norm_factor = (
        nominal[matched_sample] / integral
        if integral != 0 else 0.
    )

    if var not in norm[matched_sample]:
        norm[matched_sample][var] = {}

    norm[matched_sample][var][direction] = norm_factor

    print(f"  Variation : {var}")
    print(f"  Direction : {direction}")
    print(f"  Norm      : {norm_factor}")


# --------------------------------------------------
# 3. Print final normalization factors
# --------------------------------------------------

print("\n\n======================================")
print("FINAL NORMALIZATION FACTORS")
print("======================================")

for sample in norm:

    print(f"\nSample: {sample}")

    for var, factors in norm[sample].items():

        print(f"  {var}: {factors}")

# --------------------------------------------------
# 4. Save JSON
# --------------------------------------------------

# Create year-specific output directory
yearDir = os.path.join(outputDir, year)

os.makedirs(yearDir, exist_ok=True)

outputFile = os.path.join(yearDir,f"NormTHU_{year}_{config}.json")

with open(outputFile, 'w', encoding='utf-8') as f:
    json.dump(norm,f,ensure_ascii=False,indent=4)

print("\n======================================")
print("JSON SAVED SUCCESSFULLY")
print("======================================")
print(f"Output: {outputFile}")
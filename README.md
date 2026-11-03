# WW Cross-Section Measurement

This repository contains the configuration and workflow for the WW cross-section measurement, part of **SMP-XX-XXX**.

The analysis targets the opposite-sign, different-flavour dilepton final state (electron--muon channel), considering events with **0, 1, and 2
jets**.

This README describes the steps required to set up the environment, produce histograms, prepare and combine datacards, create the statistical workspace, and perform the signal-strength and nuisance-parameter impact fits.

------------------------------------------------------------------------

## 1. Set up the `mkShapesRDF` environment

We assume that `mkShapesRDF` and `FullRun3` are installed
in the same parent directory. For example:

``` text
Run3/
├── mkShapesRDF/
└── FullRun3/
```

Navigate to the `mkShapesRDF` directory and initialise the environment:

``` bash
cd mkShapesRDF/
source start.sh
```

------------------------------------------------------------------------

## 2. Histogram production

Navigate to the analysis configuration directory:

``` bash
cd FullRun3/Full2022EEv12/Inclusive
```

> **Note:** Check the paths defined in the aliases and configuration files. 
> Update them if necessary to match your local environment and username.

### 2.1 Compile the configuration

Compile the configuration and save the compiled JSON configuration:

``` bash
mkShapesRDF -c 1
```

Repeat this step whenever a configuration file is modified. 

### 2.2 Run a local test

For a quick test, run the analysis locally and process only two events:

``` bash
mkShapesRDF -c 1 -o 0 -f . -b 0 -l 2
```

This is useful for checking the configuration, selections, event weights, and histogram production before running over the full samples.

### 2.3 Produce histograms using HTCondor

Submit histogram-production jobs to the HTCondor batch system:

``` bash
mkShapesRDF -c 1 -o 0 -f . -b 1
```

The submission flag is also available:

``` bash
mkShapesRDF --submit
```

The `--submit` form relies on the command's default values for options. If "submit" is triggered, override the operation mode and just "submit" to batch system the creation of histograms

### 2.4 Check the batch-job status

Check the status of submitted jobs:

``` bash
mkShapesRDF -o 1 -f .
```

### 2.5 Resubmit failed jobs

Resubmit jobs that finished with errors:

``` bash
mkShapesRDF -o 1 -f . -r 1
```

Here, `-r 1` selects finished jobs with errors for resubmission.

### 2.6 Merge ROOT files

After the batch jobs have completed successfully, merge the output ROOT files:

``` bash
mkShapesRDF -o 2 -f .
```

Alternatively, use the histogram-addition flag:

``` bash
mkShapesRDF --histoadd
```

### 2.7 Plot distributions

Produce the configured distributions:

``` bash
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png
```

------------------------------------------------------------------------

## 3. Datacard production

Generate datacards for the required variables using `mkDatacard`.

Specify the output directory and the variables for which datacards should be produced:

``` bash
mkDatacard \
    --outputDirDatacard /eos/user/m/misharma/mkShapesRDF_rootfiles/FullRun3/Full2022EEv12/Inclusive/Itr0_bReq20/datacards/ \
    --onlyVariables events
```

In this example:

-   **Output directory:** Location where the datacards will be stored.
-   **Variable:** `events`, used for the inclusive cross-section
    measurement.

Update the output path to match your own EOS directory and production, default location is the current directory.

------------------------------------------------------------------------

## 4. Datacard preparation and combination

The script `utils/scripts/inclusive_xsec.sh` is used to prepare and combine the datacards for the inclusive cross-section measurement.

### 4.1 Configure the inputs

Before running the script, check the following inputs in `inclusive_xsec.sh`:

-   **`CMSSW_BASE` / Combine environment:** Ensure that the intended CMSSW release is active and that the Combine tools are available.
    Follow the [Combine installation instructions](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/#within-cmssw-recommended-for-cms-users) if needed.
-   **`CARDDIR`:** Set this to the directory containing the input datacards.

### 4.2 Run the script

From the repository's top-level directory, and outise the mkShapesRDF env execute:

``` bash
bash utils/scripts/inclusive_xsec.sh
```

Alternatively,

``` bash
./utils/scripts/inclusive_xsec.sh
```

Inspect the script to confirm the names and locations of the combined datacard outputs before proceeding.

------------------------------------------------------------------------

## 5. Workspace creation and signal-strength measurement

After preparing the combined datacard, create a statistical workspace using `text2workspace.py`.

The `multiSignalModel` configuration below maps both `WW` and `ggWW` to the same parameter, `r`. Consequently, the fit uses a **common
signal-strength modifier** for these two processes.

### 5.1 Create the workspace

``` bash
text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
    --PO verbose \
    --PO 'map=.*/WW:r[1,0,3]' \
    --PO 'map=.*/ggWW:r[1,0,3]' \
    datacard_inclusive.txt \
    -o workspace_inclusive.root
```

The parameter `r` has an initial value of 1 and is allowed to vary between 0 and 3 in the workspace.

### 5.2 Perform the signal-strength fit

Run `MultiDimFit` to extract the best-fit signal strength:

``` bash
combine -M MultiDimFit workspace_inclusive.root \
    --algo=singles \
    --robustFit=1 \
    --redefineSignalPOIs r \
    --setParameters r=1 \
    --setParameterRanges r=0.8,1.2 \
    -t -1
```

The `-t -1` option runs an expected fit using the Asimov dataset. The parameter range specified here restricts the fit to `0.8 <= r <= 1.2`.

------------------------------------------------------------------------

## 6. Nuisance-parameter impact estimation

Use the Combine Impacts workflow to evaluate the impact of individual nuisance parameters on the fitted signal strength.

### 6.1 Perform the initial fit

``` bash
combineTool.py -M Impacts \
    -d workspace_inclusive.root \
    -m 125 -n Test \
    --doInitialFit \
    -t -1 --expectSignal 1 \
    --robustFit 1
```

### 6.2 Fit individual nuisance parameters

``` bash
combineTool.py -M Impacts \
    -d workspace_inclusive.root \
    -m 125 -n Test \
    --doFit \
    -t -1 --expectSignal 1 \
    --robustFit 1 \
    --job-mode=interactive \
    --parallel=10
```

### 6.3 Collect the impact results

``` bash
combineTool.py -M Impacts \
    -d workspace_inclusive.root \
    -m 125 -n Test \
    --output json_inclusive.json \
    -t -1 --expectSignal 1 \
    --robustFit 1
```

### 6.4 Plot the impacts

``` bash
plotImpacts.py \
    -i json_inclusive.json \
    -o impacts_inclusive
```

This produces the nuisance-parameter impact plot, showing how individual nuisance parameters affect the fitted signal strength.

------------------------------------------------------------------------

## 7. References

-   [mkShapesRDF](https://github.com/latinos/mkShapesRDF)
-   [Combine ---
    HiggsAnalysis-CombinedLimit](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/)
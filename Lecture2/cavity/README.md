# OpenFOAM v2312 cavity sampling

This example extracts `U` and `p` along the vertical and horizontal centre lines of the standard `0.1 m × 0.1 m` lid-driven cavity.

## 1. Copy the dictionary into the case

```bash
cp sampleDict /path/to/cavity/system/sampleDict
cd /path/to/cavity
```

If your cavity dimensions differ from `0.1 m × 0.1 m × 0.01 m`, edit the `start` and `end` coordinates in `system/sampleDict`.

## 2. Sample the latest result

From the OpenFOAM v2312 environment, run:

```bash
postProcess -func sampleDict -fields '(U p)' -latestTime
```

The files should be written under:

```text
postProcessing/sampleDict/<latest-time>/
```

## 3. Install the plotting packages

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install numpy matplotlib jupyterlab
```

## 4. Plot from the command line

```bash
python plot_cavity_samples.py /path/to/cavity --show
```

Or open `plot_cavity_samples.ipynb`, change `CASE_DIRECTORY`, and run all cells.

> For an incompressible OpenFOAM solver, `p` is normally kinematic pressure (`p/rho`) with units of `m²/s²`. Multiply by density to obtain pressure in pascals when appropriate.

# Benchmark for Modularized Synthesis of Complex Specifications

**Authors:** Zengjie Zhang, Sofie Haesaert

## Requirements
 - Python `3.10` (or lower)
 - Required Packages: `numpy`, `treelib`, `gurobi`, `matplotlib`, `scipy`. For `conda`, they can be installed using the following commands:
```
conda install -c anaconda numpy
conda install -c conda-forge treelib
conda install -c gurobi gurobi
conda install -c conda-forge matplotlib
conda install -c anaconda scipy
```

## Toolbox stilpy

This benchmark is based on the `stlpy` toolbox (https://github.com/vincekurtz/stlpy/blob/main/README.md). Please cite the source when you develop your own benchmark.

## Instructions

- Run `main.py` to generate system trajectories;
- Run `plot_results.py` to plot the results.
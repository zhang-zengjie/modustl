# Benchmark for Modularized Synthesis of Complex Specifications

The simulation study benchmark to support the research work [Modularized Control Synthesis for Complex Signal Temporal Logic Specifications](https://ieeexplore.ieee.org/abstract/document/10383263).

## Introduction

This benchmark  considers a mobile robot required to perform a monitoring task in a rectangular space SAFETY sized $8 \times 7$ (red) with three square regions **TARGET** (yellow), **HOME**
(green), and **CHANGER** (blue) which are centered at $(2,5)$, $(6,5)$, and $(6,2)$ with the same side length $2$. The robot is described as a 2-dimensional single-integrator. The monitoring task is described as follows.
- Starting from position $(0,5)$, the robot should frequently visit **TARGET** every $5$ steps or fewer until $k=40$.
- From $k=15$ to $k=45$, once the robot leaves **HOME**,
it should get back to **HOME** within $5$ time steps.
- After $k = 20$ and before $k = 45$, it should stay in
**CHANGER** continuously for at least $3$ time steps to charge.
- The robot should always stay in the **SAFETY** region.

This benchmark aims at splitting the overall specification in time, generating local specifications with separate time intervals $(0, 15)$, $(15, 30)$, and $(30, 45)$, such that the system can be synthesized in a modularized and sequential manner. The following figure shows how the local specifications are solved in each time interval.

[![Map](map.svg)](CASE)

The following figure shows the trajectories of the agent in different stages.

[![Trajectories](trajectories.svg)](CASE)


## Requirements

**Operating system**
 - *Windows* (compatible in general, succeed on 11)
 - *Linux* (compatible in general, succeed on 20.04)
 - *MacOS* (compatible in general, succeed on 13.4.1)

 **Python Environment**

 - Python `3.11`
 - Required Packages: `numpy`, `treelib`, `matplotlib`. 

**Required Libraries**
 - `gurobipy` solver (**license** required, see [How to Get a Gurobi License](https://www.gurobi.com/solutions/licensing/))
 - `stlpy` toolbox (see [Documentation](https://stlpy.readthedocs.io/en/latest/) or [GitHub repository](https://github.com/vincekurtz/stlpy))

### Quick Installation
 
1. Install conda following this [instruction](https://conda.io/projects/conda/en/latest/user-guide/install/index.html);

2. Open the conda shell, and create an independent project environment;
```
conda create --name modustl python=3.11
```

3. In the same shell, activate the created environment
```
conda activate modustl
```

4. In the same shell, within the `modustl` environment, install the dependencies one by one
 ```
conda install -c anaconda numpy
conda install -c conda-forge treelib
conda install -c conda-forge matplotlib
```

5. In the same shell, within the `modustl` environment, install the libraries
```
python -m pip install gurobipy
pip install stlpy
```

6. Last but not least, activate the `gurobi` license (See [How To](https://www.gurobi.com/documentation/current/remoteservices/licensing.html)). Note that this project is compatible with `gurobi` Released version `11.0.1`. Keep your `gurobi` updated in case of incompatibility. 

## Running Instructions

- Run the main script `main.py`;
- Plotted figures automatically saved in the root folder.

## License

This project is with a BSD-3 license, refer to `LICENSE` for details.

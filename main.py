import numpy as np
from stlpy.solvers import GurobiMICPSolver as MICPSolver
from config import get_sys, get_specs, draw


n = 2                           # The dimension of the robot
L = 15                          # The length of each split time interval
kappa = [0, L, 2*L, 3*L]        # The split timing points
sys = get_sys(n)                # The robot dynamic model

# Generate predicates and split local specifications
gamma, bar_phi, bar_phi_t = get_specs(n, kappa)

u_limits = 1                                    # Control limits
x0 = np.array([0, 5])                           # Initial position
u_min = np.array([-u_limits, -u_limits])
u_max = np.array([u_limits, u_limits])
Q = np.zeros([n, n])                            # State cost
R = np.eye(n)                                   # Control cost

xx = []
for s in range(len(kappa)-1):

    if s < 2:
        solver = MICPSolver(bar_phi[s], sys, x0, kappa[s + 1] - kappa[s], robustness_cost=True)
    else:
        solver = MICPSolver(bar_phi[s] & bar_phi_t[s], sys, x0, kappa[s + 1] - kappa[s], robustness_cost=True)
    solver.AddControlBounds(u_min, u_max)
    solver.AddQuadraticCost(Q, R)
    x, u, _, _ = solver.Solve()
    xx += [x]
    x0 = x.T[-1]

# Draw the results
draw(xx, kappa, gamma) 
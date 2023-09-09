import numpy as np
from stlpy.solvers import GurobiMICPSolver as MICPSolver
from params import sys, n, kappa, bar_phi, bar_phi_t


u_limits = 1
x0 = np.array([0, 5])
u_min = np.array([-u_limits, -u_limits])
u_max = np.array([u_limits, u_limits])
Q = np.zeros([n, n])
R = np.eye(n)

for s in range(len(kappa)-1):

    if s < 2:
        solver = MICPSolver(bar_phi[s], sys, x0, kappa[s + 1] - kappa[s], robustness_cost=True)
    else:
        solver = MICPSolver(bar_phi[s] & bar_phi_t[s], sys, x0, kappa[s + 1] - kappa[s], robustness_cost=True)
    solver.AddControlBounds(u_min, u_max)
    solver.AddQuadraticCost(Q, R)
    x, u, _, _ = solver.Solve()
    np.save('x' + str(s + 1) + '.npy', x)
    x0 = x.T[-1]


import numpy as np
from stlpy.systems import LinearSystem
from stlpy.solvers import GurobiMICPSolver as MICPSolver
from stlpy.benchmarks.common import inside_rectangle_formula


A = np.eye(2)
B = np.eye(2)
C = np.eye(2)
D = np.zeros([2, 2])
sys = LinearSystem(A, B, C, D)

x0 = np.array([2, 6])

SAFETY = (0, 10, 0, 8)
TARGET = (3, 5, 5, 7)
HOME = (7, 9, 5, 7)
CHARGER = (7, 9, 2, 4)
PATCH = (0, 2, 0, 2)

kappa = [0, 15, 30, 45]

gamma_s = inside_rectangle_formula(SAFETY, 0, 1, 2)
gamma_t = inside_rectangle_formula(TARGET, 0, 1, 2)
gamma_h = inside_rectangle_formula(HOME, 0, 1, 2)
gamma_c = inside_rectangle_formula(CHARGER, 0, 1, 2)

bar_phi_1 = gamma_t.eventually(0, 5).always(0, 10) & gamma_t.eventually(12, 15) & gamma_s.always(0, 15)
bar_phi_2 = gamma_t.eventually(15-kappa[1], 17-kappa[1]) & gamma_t.eventually(0, 5).always(15-kappa[1], 25-kappa[1]) &\
            gamma_t.eventually(27-kappa[1], 30-kappa[1]) & gamma_h.eventually(0, 5).always(15-kappa[1], 25-kappa[1]) &\
            gamma_h.eventually(27-kappa[1], 30-kappa[1]) & gamma_s.always(15-kappa[1], 30-kappa[1])

bar_phi_3 = gamma_t.eventually(30-kappa[2], 32-kappa[2]) & gamma_h.eventually(30-kappa[2], 32-kappa[2]) &\
            gamma_t.eventually(0, 5).always(30-kappa[2], 35-kappa[2]) &\
            gamma_t.eventually(0, 5).always(30-kappa[2], 40-kappa[2]) & gamma_s.always(30-kappa[2], 45-kappa[2])


bar_phi_t_2 = gamma_c.always(0, 3).eventually(20-kappa[1], 27-kappa[1])
bar_phi_t_3 = gamma_c.always(0, 3).eventually(30-kappa[2], 42-kappa[2])


solver = MICPSolver(bar_phi_1, sys, x0, 15, robustness_cost=True)
solver.AddControlBounds(u_min=np.array([-1, -1]), u_max=np.array([1, 1]))
solver.AddQuadraticCost(Q=np.zeros([2, 2]), R=np.eye(2))

x_stage_1, u_stage_1, _, _ = solver.Solve()

solver = MICPSolver(bar_phi_2, sys, x_stage_1.T[-1], 15, robustness_cost=True)
solver.AddControlBounds(u_min=np.array([-1, -1]), u_max=np.array([1, 1]))
solver.AddQuadraticCost(Q=np.zeros([2, 2]), R=np.eye(2))

x_stage_2, u_state_2, _, _ = solver.Solve()

solver = MICPSolver(bar_phi_3 & bar_phi_t_3, sys, x_stage_2.T[-1], 15, robustness_cost=True)
solver.AddControlBounds(u_min=np.array([-1, -1]), u_max=np.array([1, 1]))
solver.AddQuadraticCost(Q=np.zeros([2, 2]), R=np.eye(2))

x_stage_3, u_state_3, _, _ = solver.Solve()

np.save('x1.npy', x_stage_1)
np.save('x2.npy', x_stage_2)
np.save('x3.npy', x_stage_3)

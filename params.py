import numpy as np
from stlpy.systems import LinearSystem
from stlpy.benchmarks.common import inside_rectangle_formula

n = 2
A = np.eye(n)
B = np.eye(n)
C = np.eye(n)
D = np.zeros([n, n])
sys = LinearSystem(A, B, C, D)

L = 15
tau = 3

SAFETY = (0, 10, 0, 8)
TARGET = (3, 5, 5, 7)
HOME = (7, 9, 5, 7)
CHARGER = (7, 9, 2, 4)

kappa = [0, L, 2*L, 3*L]

gamma_s = inside_rectangle_formula(SAFETY, 0, 1, n)
gamma_t = inside_rectangle_formula(TARGET, 0, 1, n)
gamma_h = inside_rectangle_formula(HOME, 0, 1, n)
gamma_c = inside_rectangle_formula(CHARGER, 0, 1, n)

bar_phi_1 = gamma_t.eventually(0, 5).always(0, kappa[1]-5) & gamma_t.eventually(kappa[1]-tau, kappa[1]) &\
            gamma_s.always(0, kappa[1])

bar_phi_2 = gamma_t.eventually(kappa[1]-kappa[1], kappa[1]+5-tau-kappa[1]) & \
            gamma_t.eventually(0, 5).always(kappa[1]-kappa[1], kappa[2]-5-kappa[1]) &\
            gamma_t.eventually(kappa[2]-tau-kappa[1], kappa[2]-kappa[1]) & \
            gamma_h.eventually(0, 5).always(kappa[1]-kappa[1], kappa[2]-5-kappa[1]) &\
            gamma_h.eventually(kappa[2]-tau-kappa[1], kappa[2]-kappa[1]) & \
            gamma_s.always(kappa[1]-kappa[1], kappa[2]-kappa[1])

bar_phi_3 = gamma_t.eventually(kappa[2]-kappa[2], kappa[2]+5-tau-kappa[2]) &\
            gamma_h.eventually(kappa[2]-kappa[2], kappa[2]+5-tau-kappa[2]) &\
            gamma_t.eventually(0, 5).always(kappa[2]-kappa[2], 35-kappa[2]) &\
            gamma_h.eventually(0, 5).always(kappa[2]-kappa[2], 40-kappa[2]) &\
            gamma_s.always(kappa[2]-kappa[2], kappa[3]-kappa[2])

bar_phi_t_1 = None
bar_phi_t_2 = gamma_c.always(0, 3).eventually(20-kappa[1], kappa[2]-3-kappa[1])
bar_phi_t_3 = gamma_c.always(0, 3).eventually(kappa[2]-kappa[2], kappa[3]-3-kappa[2])

bar_phi = [bar_phi_1, bar_phi_2, bar_phi_3]
bar_phi_t = [bar_phi_t_1, bar_phi_t_2, bar_phi_t_3]

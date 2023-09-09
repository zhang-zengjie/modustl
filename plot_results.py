import numpy as np
import matplotlib.pyplot as plt
from params import kappa, gamma_c, gamma_t, gamma_h


def get_coordinates(bounds):
    x_coordinates = [bounds[0], bounds[1], bounds[1], bounds[0]]
    y_coordinates = [bounds[2], bounds[2], bounds[3], bounds[3]]
    return x_coordinates, y_coordinates


SAFETY = (2, 10, 1, 8)
TARGET = (3, 5, 5, 7)
HOME = (7, 9, 5, 7)
CHARGER = (7, 9, 2, 4)
PATCH = (0, 2, 0, 2)

SAFETY_COLOR = [1, 0.9, 0.9]
TARGET_COLOR = [1, 1, 0.9]
HOME_COLOR = [0.9, 1, 0.9]
CHARGER_COLOR = [0.9, 0.95, 1]

x_stage_1 = np.load('x1.npy')
x_stage_2 = np.load('x2.npy')
x_stage_3 = np.load('x3.npy')

STATE_1_COLOR = [0.5, 0, 0]
STATE_2_COLOR = [0, 0.25, 0.8]
STATE_3_COLOR = [0.8, 0.4, 0]

plt.fill(*get_coordinates(SAFETY), color=SAFETY_COLOR)
plt.fill(*get_coordinates(TARGET), color=TARGET_COLOR)
plt.fill(*get_coordinates(HOME), color=HOME_COLOR)
plt.fill(*get_coordinates(CHARGER), color=CHARGER_COLOR)
plt.fill(*get_coordinates(PATCH), color=[1, 1, 1])

ps, = plt.plot(x_stage_1[0][0], x_stage_1[1][0], marker='o', color=STATE_1_COLOR, linewidth=2, markersize=8)
p1, = plt.plot(x_stage_1[0], x_stage_1[1], marker='o', color=STATE_1_COLOR, linewidth=2, markersize=5)
p2, = plt.plot(x_stage_2[0], x_stage_2[1], marker='o', color=STATE_2_COLOR, linewidth=2, markersize=5)
p3, = plt.plot(x_stage_3[0], x_stage_3[1], marker='o', color=STATE_3_COLOR, linewidth=2, markersize=5)
pe, = plt.plot(x_stage_3[0][-1], x_stage_3[1][-1], marker='o', color=STATE_3_COLOR, linewidth=2, markersize=8)
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.legend([ps, p1, p2, p3, pe],
           ['Initial position', 'Trajectory stage 1', 'Trajectory stage 2', 'Trajectory stage 3', 'Ending position'],
           loc='lower left')

fig, axs = plt.subplots(2)

axs[0].plot(np.arange(0, kappa[1]+1), x_stage_1[0], color=STATE_1_COLOR, linewidth=2.5, linestyle='solid')
axs[1].plot(np.arange(0, kappa[1]+1), x_stage_1[1], color=STATE_1_COLOR, linewidth=2.5, linestyle='solid')

axs[0].plot(np.arange(kappa[1], kappa[2]+1), x_stage_2[0], color=STATE_2_COLOR, linewidth=2.5, linestyle='solid')
axs[1].plot(np.arange(kappa[1], kappa[2]+1), x_stage_2[1], color=STATE_2_COLOR, linewidth=2.5, linestyle='solid')

axs[0].plot(np.arange(kappa[2], kappa[3]+1), x_stage_3[0], color=STATE_3_COLOR, linewidth=2.5, linestyle='solid')
axs[1].plot(np.arange(kappa[2], kappa[3]+1), x_stage_3[1], color=STATE_3_COLOR, linewidth=2.5, linestyle='solid')

x_complete = np.concatenate((x_stage_1.T, x_stage_2.T[1:], x_stage_3.T[1:]))

for i in range(kappa[3]):
    if gamma_t.robustness(y=np.array([x_complete[i]]).T, t=0) >= 0:
        axs[0].fill(*get_coordinates((i, i + 1, 0, 12)), color=TARGET_COLOR)
        axs[1].fill(*get_coordinates((i, i + 1, 0, 12)), color=TARGET_COLOR)
    elif gamma_h.robustness(y=np.array([x_complete[i]]).T, t=0) >= 0:
        axs[0].fill(*get_coordinates((i, i + 1, 0, 12)), color=HOME_COLOR)
        axs[1].fill(*get_coordinates((i, i + 1, 0, 12)), color=HOME_COLOR)
    elif gamma_c.robustness(y=np.array([x_complete[i]]).T, t=0) >= 0:
        axs[0].fill(*get_coordinates((i, i + 1, 0, 12)), color=CHARGER_COLOR)
        axs[1].fill(*get_coordinates((i, i + 1, 0, 12)), color=CHARGER_COLOR)

axs[0].set_xlim([0, kappa[3]])
axs[0].set_ylim([0, 12])
axs[1].set_xlim([0, kappa[3]])
axs[1].set_ylim([0, 12])

plt.show()

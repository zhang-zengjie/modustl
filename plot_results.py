import numpy as np
import matplotlib.pyplot as plt


L = 15


def get_coordinates(bounds):
    x_coordinates = [bounds[0], bounds[1], bounds[1], bounds[0]]
    y_coordinates = [bounds[2], bounds[2], bounds[3], bounds[3]]
    return x_coordinates, y_coordinates


SAFETY = (2, 10, 1, 8)
TARGET = (3, 5, 5, 7)
HOME = (7, 9, 5, 7)
CHARGER = (7, 9, 2, 4)
PATCH = (0, 2, 0, 2)

x_stage_1 = np.load('x1.npy')
x_stage_2 = np.load('x2.npy')
x_stage_3 = np.load('x3.npy')


plt.fill(*get_coordinates(SAFETY), color=[1, 0.9, 0.9])
plt.fill(*get_coordinates(TARGET), color=[1, 1, 0.9])
plt.fill(*get_coordinates(HOME), color=[0.9, 1, 0.9])
plt.fill(*get_coordinates(CHARGER), color=[0.9, 0.95, 1])
plt.fill(*get_coordinates(PATCH), color=[1, 1, 1])

ps, = plt.plot(x_stage_1[0][0], x_stage_1[1][0], marker='o', color=[0.5, 0, 0], linewidth=2, markersize=8)
p1, = plt.plot(x_stage_1[0], x_stage_1[1], marker='o', color=[0.5, 0, 0], linewidth=2, markersize=5)
p2, = plt.plot(x_stage_2[0], x_stage_2[1], marker='o', color=[0, 0.25, 0.8], linewidth=2, markersize=5)
p3, = plt.plot(x_stage_3[0], x_stage_3[1], marker='o', color=[0.8, 0.4, 0], linewidth=2, markersize=5)
pe, = plt.plot(x_stage_3[0][-1], x_stage_3[1][-1], marker='o', color=[0.8, 0.4, 0], linewidth=2, markersize=8)
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.legend([ps, p1, p2, p3, pe],
           ['Initial position', 'Trajectory stage 1', 'Trajectory stage 2', 'Trajectory stage 3', 'Ending position'],
           loc='lower left')

fig, axs = plt.subplots(2)

axs[0].plot(np.arange(0, L+1), x_stage_1[0])
axs[1].plot(np.arange(0, L+1), x_stage_1[1])

axs[0].plot(np.arange(L, 2*L+1), x_stage_2[0])
axs[1].plot(np.arange(L, 2*L+1), x_stage_2[1])

axs[0].plot(np.arange(2*L, 3*L+1), x_stage_3[0])
axs[1].plot(np.arange(2*L, 3*L+1), x_stage_3[1])

plt.show()

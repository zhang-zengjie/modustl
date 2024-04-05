import numpy as np
from stlpy.systems import LinearSystem
import matplotlib.pyplot as plt
from stlpy.benchmarks.common import inside_rectangle_formula


REGION = {
    's': (0, 8, 0, 7),     # REGION['s']
    't': (1, 3, 4, 6),     # REGION['t']
    'h': (5, 7, 4, 6),     # REGION['h']
    'c': (5, 7, 1, 3)      # REGION['c']
}


def get_coordinates(bounds):
    x_coordinates = [bounds[0], bounds[1], bounds[1], bounds[0]]
    y_coordinates = [bounds[2], bounds[2], bounds[3], bounds[3]]
    return x_coordinates, y_coordinates


def get_sys(n):

    A = np.eye(n)
    B = np.eye(n)
    C = np.eye(n)
    D = np.zeros([n, n])
    sys = LinearSystem(A, B, C, D)

    return sys


def get_specs(n, kappa):

    tau = len(kappa)-1

    gamma = {key: inside_rectangle_formula(value, 0, 1, n) for key, value in REGION.items()}

    bar_phi_1 = gamma['t'].eventually(0, 5).always(0, kappa[1]-5) & gamma['t'].eventually(kappa[1]-tau, kappa[1]) &\
                gamma['s'].always(0, kappa[1])

    bar_phi_2 = gamma['t'].eventually(kappa[1]-kappa[1], kappa[1]+5-tau-kappa[1]) & \
                gamma['t'].eventually(0, 5).always(kappa[1]-kappa[1], kappa[2]-5-kappa[1]) &\
                gamma['t'].eventually(kappa[2]-tau-kappa[1], kappa[2]-kappa[1]) & \
                gamma['h'].eventually(0, 5).always(kappa[1]-kappa[1], kappa[2]-5-kappa[1]) &\
                gamma['h'].eventually(kappa[2]-tau-kappa[1], kappa[2]-kappa[1]) & \
                gamma['s'].always(kappa[1]-kappa[1], kappa[2]-kappa[1])

    bar_phi_3 = gamma['t'].eventually(kappa[2]-kappa[2], kappa[2]+5-tau-kappa[2]) &\
                gamma['h'].eventually(kappa[2]-kappa[2], kappa[2]+5-tau-kappa[2]) &\
                gamma['t'].eventually(0, 5).always(kappa[2]-kappa[2], 35-kappa[2]) &\
                gamma['h'].eventually(0, 5).always(kappa[2]-kappa[2], 40-kappa[2]) &\
                gamma['s'].always(kappa[2]-kappa[2], kappa[3]-kappa[2])

    bar_phi_t_1 = None
    bar_phi_t_2 = gamma['c'].always(0, 3).eventually(20-kappa[1], kappa[2]-3-kappa[1])
    bar_phi_t_3 = gamma['c'].always(0, 3).eventually(kappa[2]-kappa[2], kappa[3]-3-kappa[2])

    bar_phi = [bar_phi_1, bar_phi_2, bar_phi_3]
    bar_phi_t = [bar_phi_t_1, bar_phi_t_2, bar_phi_t_3]

    return gamma, bar_phi, bar_phi_t


def draw(x, kappa, gamma):

    CM = {
        's': [1, 0.9, 0.9],
        't': [1, 1, 0.9],
        'h': [0.9, 1, 0.9],
        'c': [0.9, 0.95, 1]
    }

    x_stage_1, x_stage_2, x_stage_3 = x

    STATE_1_COLOR = [0.5, 0, 0]
    STATE_2_COLOR = [0, 0.25, 0.8]
    STATE_3_COLOR = [0.8, 0.4, 0]

    plt.fill(*get_coordinates(REGION['s']), color=CM['s'])
    plt.fill(*get_coordinates(REGION['t']), color=CM['t'])
    plt.fill(*get_coordinates(REGION['h']), color=CM['h'])
    plt.fill(*get_coordinates(REGION['c']), color=CM['c'])

    plt.text((REGION['t'][0]+REGION['t'][1])/2, (REGION['t'][2]+REGION['t'][3])/2+0.2, 'TARGET', fontsize=12, horizontalalignment='center')
    plt.text((REGION['h'][0]+REGION['h'][1])/2, (REGION['h'][2]+REGION['h'][3])/2+0.2, 'HOME', fontsize=12, horizontalalignment='center')
    plt.text((REGION['c'][0]+REGION['c'][1])/2, (REGION['c'][2]+REGION['c'][3])/2+0.2, 'CHARGER', fontsize=12, horizontalalignment='center')
    plt.text(REGION['s'][0]+0.1, REGION['s'][3]-0.1, 'SAFETY', fontsize=12, horizontalalignment='left', verticalalignment='top')


    ps, = plt.plot(x_stage_1[0][0], x_stage_1[1][0], marker='o', color=STATE_1_COLOR, linewidth=2, markersize=8)
    p1, = plt.plot(x_stage_1[0], x_stage_1[1], marker='o', color=STATE_1_COLOR, linewidth=2, markersize=5)
    p2, = plt.plot(x_stage_2[0], x_stage_2[1], marker='o', color=STATE_2_COLOR, linewidth=2, markersize=5)
    p3, = plt.plot(x_stage_3[0], x_stage_3[1], marker='o', color=STATE_3_COLOR, linewidth=2, markersize=5)
    pe, = plt.plot(x_stage_3[0][-1], x_stage_3[1][-1], marker='o', color=STATE_3_COLOR, linewidth=2, markersize=8)
    plt.xlim([0, REGION['s'][1]])
    plt.ylim([0, REGION['s'][3]])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend([ps, p1, p2, p3, pe],
            ['Initial position', 'Trajectory stage 1', 'Trajectory stage 2', 'Trajectory stage 3', 'Ending position'],
            loc='lower left')

    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    plt.savefig('map.svg', bbox_inches='tight', pad_inches=0.1, transparent=True)

    _, axs = plt.subplots(2)

    axs[0].plot(np.arange(0, kappa[1]+1), x_stage_1[0], color=STATE_1_COLOR, linewidth=2.5, linestyle='solid')
    axs[1].plot(np.arange(0, kappa[1]+1), x_stage_1[1], color=STATE_1_COLOR, linewidth=2.5, linestyle='solid')

    axs[0].plot(np.arange(kappa[1], kappa[2]+1), x_stage_2[0], color=STATE_2_COLOR, linewidth=2.5, linestyle='solid')
    axs[1].plot(np.arange(kappa[1], kappa[2]+1), x_stage_2[1], color=STATE_2_COLOR, linewidth=2.5, linestyle='solid')

    axs[0].plot(np.arange(kappa[2], kappa[3]+1), x_stage_3[0], color=STATE_3_COLOR, linewidth=2.5, linestyle='solid')
    axs[1].plot(np.arange(kappa[2], kappa[3]+1), x_stage_3[1], color=STATE_3_COLOR, linewidth=2.5, linestyle='solid')

    x_complete = np.concatenate((x_stage_1.T, x_stage_2.T[1:], x_stage_3.T[1:]))

    for i in range(kappa[3]):
        if gamma['t'].robustness(y=np.array([x_complete[i]]).T, t=0) >= 0:
            axs[0].fill(*get_coordinates((i, i + 1, 0, 12)), color=CM['t'])
            axs[1].fill(*get_coordinates((i, i + 1, 0, 12)), color=CM['t'])
        elif gamma['h'].robustness(y=np.array([x_complete[i]]).T, t=0) >= 0:
            axs[0].fill(*get_coordinates((i, i + 1, 0, 12)), color=CM['h'])
            axs[1].fill(*get_coordinates((i, i + 1, 0, 12)), color=CM['h'])
        elif gamma['c'].robustness(y=np.array([x_complete[i]]).T, t=0) >= 0:
            axs[0].fill(*get_coordinates((i, i + 1, 0, 12)), color=CM['c'])
            axs[1].fill(*get_coordinates((i, i + 1, 0, 12)), color=CM['c'])

    axs[0].set_xlim([0, kappa[3]])
    axs[0].set_ylim([REGION['s'][2], REGION['s'][3]-1])
    axs[1].set_xlim([0, kappa[3]])
    axs[1].set_ylim([REGION['s'][2], REGION['s'][3]-1])

    axs[0].set_ylabel(r'$x$')
    axs[1].set_ylabel(r'$y$')
    axs[1].set_xlabel(r'$k$')

    plt.savefig('trajectories.svg', bbox_inches='tight', pad_inches=0.1, transparent=True)

    plt.show()
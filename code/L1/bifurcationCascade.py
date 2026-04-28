#!/usr/bin/env python3
# created by Group Supermodels in VT2026
# for the course Modelling of Complex Systems at Uppsala University
# Group Members:
# Juan Rodriguez
# Björk Lucas
# Vootele Mets
# Marco Malosti
# Sofia Fernandes
# David Weingut
import numpy as np
from common import coupled_map
import matplotlib.pyplot as plt

#defining the constants as given in the exercise
r1 = 3.1
epsi = 0.3
r2 = np.linspace(2.8, 3.97, 800)
xy_start = np.array([0.2, 0.6])
steps = 400
discard = 150


def calc_timeline(xy0, r2, steps, discard):
    '''function for calculation of a set amount of steps of the logical map
    xy0: array of initial x and y value
    r2: r2 value used for the specific timeline
    steps: number of iterations that are calculated 
    discard: number of iterations from the beginning of the calculation that are discarded    
    '''
    xy_timeline = [xy0]
    for i in range(steps):
        xy_new = coupled_map(xy_timeline[-1], [r1, r2, epsi])
        xy_timeline.append(xy_new)
    return xy_timeline[discard:]


if __name__ == "__main__":
    for element in r2:
        new_timeline = calc_timeline(xy_start, element, steps, discard) #calculating timeline for each r2 value
        x_vals = [xy[0] for xy in new_timeline]
        plt.plot([element] * (len(x_vals)), x_vals, '.') #plotting each timeline 
    plt.xlabel('$r_2$')
    plt.ylabel('$x*$')
    plt.title('Bifurcation Cascade ($r_1=3.1$, $\\epsilon = 0.3$)')
    plt.grid()
    plt.savefig('figures/bifurcationcascade.png', dpi=300)
    plt.show()

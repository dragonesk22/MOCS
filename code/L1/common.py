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


def coupled_map(xy, ps):
    """
    do one step of the coupled map
    xy: np.array [x_n, y_n]
    ps: array [r1, r2, epsilon], same order as in the instructions
    """
    x, y = xy
    r1, r2, epsi = ps
    r1xx = r1 * x * (1 - x)
    r2yy = r2 * y * (1 - y)
    return np.array([(1 - epsi) * r1xx + epsi * r2yy,
                     (1 - epsi) * r2yy + epsi * r1xx])

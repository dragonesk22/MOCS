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

def add_pattern(x, pattern, h, k):
    """
    :param x:
    :param pattern:
    :param h: y coordinate
    :param k: x coordinate
    """
    pattern = np.asarray(pattern)

    # Grid-based pattern (2D array)
    if pattern.ndim == 2:
        rows, cols = pattern.shape
        for i in range(rows):
            for j in range(cols):
                if pattern[i, j] == 1:
                    x[h+i, k+j] = 1

    # Coordinate list [(i,j), ...]
    else:
        for i, j in pattern:
            x[h+i, k+j] = 1

def transform_pattern(pattern, rot=0, flip_lr=False, flip_ud=False):
    p = np.array(pattern, dtype=np.uint8)
    if rot:
        p = np.rot90(p, k=rot)
    if flip_lr:
        p = np.fliplr(p)
    if flip_ud:
        p = np.flipud(p)

    return p
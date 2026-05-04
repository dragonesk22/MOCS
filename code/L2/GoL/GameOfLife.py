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
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)
import numpy as np
from scipy.ndimage import convolve
import matplotlib.pyplot as plt
from matplotlib import rc
from GoLogic import AND, OR, NOT
rc('text', usetex=True)
rc('font', family='serif', size=12)



def F(X, K=np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
], dtype=np.uint8), mode="constant"):
    """
    :param X: 2D array data structure for rectangular lattice graph
    :param K: 3x3 kernel
    :return: Non-linear update of X
    """
    # Linear map
    if mode == "constant":
        N = convolve(X, K, mode=mode, cval=0)
    else:
        assert mode == "wrap", "mode must be 'wrap' or 'constant'"
        N = convolve(X, K, mode=mode)
    # Non-linear map
    return ((N == 3) | ((X == 1) & (N == 2))).astype(np.uint8)


def load_live_cells(filename, n):
    """can run GoL from an external file with one (x,y) per line"""
    grid = np.zeros((n, n), dtype=np.uint8)
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or not line.startswith("("):
                continue
            xs, ys = line.strip("()").split(",")
            grid[int(ys), int(xs)] = 1
    return grid


n = 400
# If a coordinate file is supplied (e.g. AND.txt / OR.txt / NOT.txt) load it,
# otherwise fall back to building the gate in code.
if len(sys.argv) > 1:
    x = load_live_cells(sys.argv[1], n)
else:
    x = np.zeros((n, n), dtype=np.uint8)
    x = AND(x, A=1, B=1)

nsteps = 1000
X = [None]*nsteps
X[0] = x.copy()
for k in range(nsteps-1):
    X[k+1] = F(X[k])


plt.ion()
fig, ax = plt.subplots()
im = ax.imshow(x, cmap="binary", interpolation="nearest")
ax.set_xticks([])
ax.set_yticks([])

for k in range(nsteps):
    im.set_data(X[k])
    plt.pause(0.025)

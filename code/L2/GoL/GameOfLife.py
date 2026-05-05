#!/usr/bin/env python3
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
    if mode == "constant":
        N = convolve(X, K, mode=mode, cval=0)
    else:
        assert mode == "wrap", "mode must be 'wrap' or 'constant'"
        N = convolve(X, K, mode=mode)

    return ((N == 3) | ((X == 1) & (N == 2))).astype(np.uint8)


def load_live_cells(filename, n):
    grid = np.zeros((n, n), dtype=np.uint8)
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or not line.startswith("("):
                continue
            xs, ys = line.strip("()").split(",")
            grid[int(ys), int(xs)] = 1
    return grid


def build_gate(gate, n, A, B=0):
    x = np.zeros((n, n), dtype=np.uint8)

    if gate == "AND":
        x = AND(x, A=A, B=B)
    elif gate == "OR":
        x = OR(x, A=A, B=B)
    elif gate == "NOT":
        x = NOT(x, A=A)

    return x


n = 400
nsteps = 1000
gate = "NOT"
plt.ion()

if gate in ["AND", "OR"]:
    cases = [(0, 0), (0, 1), (1, 0), (1, 1)]

    fig, axs = plt.subplots(2, 2, figsize=(10, 10), constrained_layout=True)
    axs = axs.flatten()

    states = []
    images = []

    for i, (A, B) in enumerate(cases):
        x = build_gate(gate, n, A, B)
        states.append(x)

        im = axs[i].imshow(x, cmap="binary", interpolation="nearest", origin="upper")
        images.append(im)

        axs[i].set_title(f"{gate}: $A={A}$, $B={B}$", fontsize=14)
        axs[i].set_xlabel("$x$")
        axs[i].set_ylabel("$y$")
        axs[i].set_xlim(0, 160)
        axs[i].set_ylim(100, 0)

    suptitle = fig.suptitle(f"{gate}-gate, $t = 0$", fontsize=18)

    # Initial draw once, then cache the background for fast redraws
    fig.canvas.draw()
    background = fig.canvas.copy_from_bbox(fig.bbox)

    for k in range(nsteps):
        # Update the automaton first
        states = [F(s) for s in states]

        # Fast redraw path
        fig.canvas.restore_region(background)

        for im, s, ax in zip(images, states, axs):
            im.set_data(s)
            ax.draw_artist(im)

        suptitle.set_text(f"{gate}-gate, $t = {k}$")
        fig.draw_artist(suptitle)

        fig.canvas.blit(fig.bbox)
        fig.canvas.flush_events()

        if k == 464 or k == 465:
            fig.savefig(f"./{gate}_{k}.pdf", format="pdf", bbox_inches="tight")

elif gate == "NOT":
    cases = [0, 1]

    fig, axs = plt.subplots(1, 2, figsize=(10, 5), constrained_layout=True)

    states = []
    images = []

    for i, A in enumerate(cases):
        x = build_gate(gate, n, A)
        states.append(x)

        im = axs[i].imshow(x, cmap="binary", interpolation="nearest", origin="upper")
        images.append(im)

        axs[i].set_title(f"{gate}: $A={A}$", fontsize=14)
        axs[i].set_xlabel("$x$")
        axs[i].set_ylabel("$y$")
        axs[i].set_xlim(0, 100)
        axs[i].set_ylim(35, 0)

    for k in range(nsteps):
        for i in range(len(states)):
            images[i].set_data(states[i])

        fig.suptitle(f"{gate}–gate, $t = {k}$", fontsize=18)
        plt.pause(0.025)

        if k == 488:
            plt.savefig(f"./{gate}_{k}.pdf", format="pdf", bbox_inches="tight")

        for i in range(len(states)):
            states[i] = F(states[i])  # Linear map


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
X = [None] * nsteps
X[0] = x.copy()
for k in range(nsteps - 1):
    X[k + 1] = F(X[k])

plt.ion()
fig, ax = plt.subplots()
im = ax.imshow(x, cmap="binary", interpolation="nearest")
ax.set_xticks([])
ax.set_yticks([])

for k in range(nsteps):
    im.set_data(X[k])
    plt.pause(0.025)

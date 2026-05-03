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
from scipy.ndimage import convolve
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc
from RLE import parse_rle

gosper_gun ="""
#N Gosper glider gun
#C This was the first gun discovered.
#C As its name suggests, it was discovered by Bill Gosper.
x = 36, y = 9, rule = B3/S23
24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o$2o8bo3bob2o4b
obo$10bo5bo7bo$11bo3bo$12b2o!
"""

eater1 = """
x = 4, y = 4, rule = B3/S23
2o$bo$bobo$2b2o!
"""

rc('text', usetex=True)
rc('font', family='serif', size=12)


def add_pattern(x, pattern, h, k):
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

def F(X, K=np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
], dtype=np.uint8)):
    N = convolve(X, K, mode="constant", cval=0)
    return ((N == 3) | ((X == 1) & (N == 2))).astype(np.uint8)


# ── Pre-compute all states ────────────────────────────────────────────────────
def AND_ish(x):
    """
    Useful commands for transformations:
    flipud(x) "Flip array in the up/down direction."
    np.fliplr(x) "Reverse the order of elements along axis 1 (left/right)"
    np.rot90(x) "Rotate array counterclockwise"
    np.roll(x, shift=-1, axis=0)   # shift up
    np.roll(x, shift=+1, axis=0)   # shift down
    np.roll(x, shift=+1, axis=1)   # shift right
    np.roll(x, shift=-1, axis=1)   # shift left
    """
    add_pattern(x, parse_rle(gosper_gun), 50,50)
    x = np.fliplr(x)
    add_pattern(x, parse_rle(gosper_gun), 0, 40)
    add_pattern(x, parse_rle(gosper_gun), 0, 80)
    return x

def NOT(x, A=1):
    gun = parse_rle(gosper_gun)
    gun_t = transform_pattern(gun, rot=0, flip_lr=True, flip_ud=False)
    add_pattern(x, gun_t, 100, 150)

    if A == 1:
        #add_pattern(x, parse_rle(gosper_gun), 60, 40)
        add_pattern(x, parse_rle(gosper_gun), 1, 0)

    return x

def NOT2(x, A=0):
    gun = parse_rle(gosper_gun)
    eater = parse_rle(eater1)


    # ── Input A lane ─────────────────────────
    y_A, x_A = 1, 0
    add_pattern(x, parse_rle(gosper_gun), y_A, x_A)
    y_eA0, x_eA0 = y_A + 13, x_A + 27

    if A == 0:
        eater_A0 = transform_pattern(eater, rot=2, flip_lr=False, flip_ud=False)
        add_pattern(x, eater_A0, y_eA0, x_eA0)
    # ── D lane ─────────────────────────
    gun_t = transform_pattern(gun, rot=0, flip_lr=True, flip_ud=False)
    y_D, x_D = y_A-1, x_A+45
    add_pattern(x, gun_t, y_D, x_D)
    return x


def OR(x, A=1, B=1):
    gun = parse_rle(gosper_gun)
    eater = parse_rle(eater1)
    add_pattern(x, gun, 50, 50)
    x = np.fliplr(x)
    x = np.roll(x, shift=-50, axis=0)   # shift up
    x = np.roll(x, shift=-143, axis=1)  # shift left
    add_pattern(x, gun, 1, 0)

    if A == 1:
        add_pattern(x, gun, 1, 42)   # Input A
        eater_t = transform_pattern(
            eater,
            rot=2,
            flip_lr=False,
            flip_ud=False
        )
        add_pattern(x, eater_t, 71, 126)
    if B == 1:
        add_pattern(x, gun, 0, 98)   # Input B

    return x

def AND(x, A=1, B=1):
    gun = np.array(parse_rle(gosper_gun), dtype=np.uint8)
    eater = np.array(parse_rle(eater1), dtype=np.uint8)

    # ── Input A lane ─────────────────────────
    y_A, x_A = 1, 0
    if A == 1:
        add_pattern(x, gun, y_A, x_A)
    else:
        add_pattern(x, gun, y_A, x_A)
        y_eA, x_eA = 12 , 26
        eater_A = transform_pattern(eater, rot=2)
        add_pattern(x, eater_A, y_eA, x_eA)

    # ── Input B lane ─────────────────────────
    y_B, x_B = 0, 56
    if B == 1:
        add_pattern(x, gun, y_B, x_B)
    else:
        add_pattern(x, gun, y_B, x_B)
        y_eB, x_eB = 13, 83
        eater_B = transform_pattern(eater, rot=2)
        add_pattern(x, eater_B, y_eB, x_eB)

    y_eC, x_eC = 64, 54
    ereater_C = transform_pattern(eater, rot=2, flip_lr=True)
    add_pattern(x, ereater_C, y_eC, x_eC)

    # ── Output stream ────────────────────────
    y_D, x_D = 0, 101
    gun_t = transform_pattern(gun, rot=0, flip_lr=True, flip_ud=False)
    add_pattern(x, gun_t, y_D, x_D)

    return x



def OR2(x, A=1, B=0):
    gun = parse_rle(gosper_gun)
    eater = parse_rle(eater1)

    # ── Left Lane ─────────────────────────
    y_D1, x_D1 = 1, 0
    add_pattern(x, gun, y_D1, x_D1)

    # ── Input A lane ─────────────────────────
    y_A, x_A = 1, 42
    add_pattern(x, gun, y_A, x_A)
    y_eA1, x_eA1 = 71, 126
    y_eA0, x_eA0 = y_A + 13, x_A + 27
    if A == 1:
        eater_A1 = transform_pattern(eater, rot=2, flip_lr=False, flip_ud=False)
        add_pattern(x, eater_A1, y_eA1, x_eA1)
    else:
        eater_A0 = transform_pattern(eater, rot=2, flip_lr=False, flip_ud=False)
        add_pattern(x, eater_A0, y_eA0, x_eA0)

    # ── Input B lane ─────────────────────────
    y_B, x_B = 0, 98
    add_pattern(x, gun, y_B, x_B)
    y_eB0, x_eB0 = y_B + 13, x_B + 27
    if B == 0:
        eater_B0 = transform_pattern(eater, rot=2, flip_lr=False, flip_ud=False)
        add_pattern(x, eater_B0, y_eB0, x_eB0)

    # ── Right Lane ─────────────────────────
    y_D2, x_D2 = 0, 143
    gun_t = transform_pattern(gun, rot=0, flip_lr=True, flip_ud=False)
    add_pattern(x, gun_t, y_D2, x_D2)
    return x

def AND2(x, A=1, B=1):
    gun = np.array(parse_rle(gosper_gun), dtype=np.uint8)
    eater = np.array(parse_rle(eater1), dtype=np.uint8)

    # ── Input A lane ─────────────────────────
    y_A, x_A = 1, 0
    add_pattern(x, gun, y_A, x_A)
    #y_eA, x_eA = 13, 26
    y_eA, x_eA = y_A + 13, x_A + 27

    if A == 0:
        eater_A = transform_pattern(eater, rot=2)
        add_pattern(x, eater_A, y_eA, x_eA)

    # ── Input B lane ─────────────────────────
    y_B, x_B = 0, 56
    add_pattern(x, gun, y_B, x_B)
    y_eB, x_eB = y_B + 13, x_B + 27
    #y_eB, x_eB = 13, 83

    if B == 0:
        eater_B = transform_pattern(eater, rot=2)
        add_pattern(x, eater_B, y_eB, x_eB)

    y_eC, x_eC = 64, 54
    eater_C = transform_pattern(eater, rot=2, flip_lr=True)
    add_pattern(x, eater_C, y_eC, x_eC)

    # ── Output stream ────────────────────────
    y_D, x_D = 0, 101
    gun_t = transform_pattern(gun, rot=0, flip_lr=True, flip_ud=False)
    add_pattern(x, gun_t, y_D, x_D)

    return x





n = 400
x = np.zeros((n, n), dtype=np.uint8)
#x = OR(x, A=1, B=1)
#x = NOT(x, A=1)
#x = AND2(x, A=1, B=0)
x = NOT2(x)


nsteps = 1000
X = [None] * nsteps
X[0] = x.copy()
for k in range(nsteps - 1):
    X[k + 1] = F(X[k])


# ── Playback state ────────────────────────────────────────────────────────────
# Generated by ChatGPT for debugging

state = {'frame': 0, 'paused': False}


def _update_title():
    status = 'PAUSED' if state['paused'] else 'PLAYING'
    ax.set_title(
        f'step {state["frame"]:04d} / {nsteps - 1}   [{status}]  '
        r'$\leftarrow$ / $\rightarrow$ step   SPACE pause',
        fontsize=9
    )
    # Title is not part of blit artists, so force a full draw on title changes
    fig.canvas.draw_idle()


def on_key(event):
    if event.key == ' ':
        state['paused'] = not state['paused']
        if state['paused']:
            ani.event_source.stop()
        else:
            ani.event_source.start()
        _update_title()

    elif event.key == 'right':
        state['paused'] = True
        ani.event_source.stop()
        state['frame'] = min(state['frame'] + 1, nsteps - 1)
        im.set_data(X[state['frame']])
        _update_title()

    elif event.key == 'left':
        state['paused'] = True
        ani.event_source.stop()
        state['frame'] = max(state['frame'] - 1, 0)
        im.set_data(X[state['frame']])
        _update_title()


# ── Figure setup ──────────────────────────────────────────────────────────────

fig, ax = plt.subplots()
# Use nearest-neighbour and float32 data — avoids internal dtype conversions
im = ax.imshow(X[0].astype(np.float32), cmap='binary',
               interpolation='nearest', vmin=0, vmax=1,
               animated=True)          # <-- marks this artist for blit
ax.set_xticks([])
ax.set_yticks([])
_update_title()

fig.canvas.mpl_connect('key_press_event', on_key)


# ── Animation ─────────────────────────────────────────────────────────────────

def animate(_):
    if state['frame'] < nsteps - 1:
        state['frame'] += 1
    im.set_data(X[state['frame']])
    return (im,)          # blit=True only redraws these artists


ani = FuncAnimation(
    fig,
    animate,
    interval=25,          # ms between frames — tune to taste
    blit=True,            # only repaint the image, not axes/title/etc.
    cache_frame_data=False
)

plt.show()
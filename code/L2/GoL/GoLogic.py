from RLE import parse_rle
from pattern_processing import add_pattern, transform_pattern
import numpy as np

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

def NOT(x, A=0):
    gun = parse_rle(gosper_gun)
    eater = parse_rle(eater1)

    # ── Input A lane ─────────────────────────
    y_A, x_A = 1, 0
    add_pattern(x, parse_rle(gosper_gun), y_A, x_A)
    y_eA0, x_eA0 = y_A + 13, x_A + 27

    if A == 0:
        eater_A0 = transform_pattern(eater, rot=2, flip_lr=False, flip_ud=False)
        add_pattern(x, eater_A0, y_eA0, x_eA0)
    # ── Right lane ─────────────────────────
    gun_t = transform_pattern(gun, rot=0, flip_lr=True, flip_ud=False)
    y_D, x_D = y_A-1, x_A+45
    add_pattern(x, gun_t, y_D, x_D)
    return x


def OR(x, A=1, B=0):
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
    y_eB0, x_eB0 = y_B + 13, x_B + 27 # B-eater
    if B == 0:
        eater_B0 = transform_pattern(eater, rot=2, flip_lr=False, flip_ud=False)
        add_pattern(x, eater_B0, y_eB0, x_eB0)

    # ── Right Lane ─────────────────────────
    y_D2, x_D2 = 0, 143
    gun_t = transform_pattern(gun, rot=0, flip_lr=True, flip_ud=False)
    add_pattern(x, gun_t, y_D2, x_D2)
    return x



def AND(x, A=1, B=1):
    gun = np.array(parse_rle(gosper_gun), dtype=np.uint8)
    eater = np.array(parse_rle(eater1), dtype=np.uint8)

    # ── Input A lane ─────────────────────────
    y_A, x_A = 1, 0
    add_pattern(x, gun, y_A, x_A)
    y_eA, x_eA = y_A + 13, x_A + 27

    if A == 0:
        eater_A = transform_pattern(eater, rot=2)
        add_pattern(x, eater_A, y_eA, x_eA)

    # ── Input B lane ─────────────────────────
    y_B, x_B = 0, 56
    add_pattern(x, gun, y_B, x_B)
    y_eB, x_eB = y_B + 13, x_B + 27

    if B == 0:
        eater_B = transform_pattern(eater, rot=2)
        add_pattern(x, eater_B, y_eB, x_eB)

    y_eC, x_eC = 64, 54
    eater_C = transform_pattern(eater, rot=2, flip_lr=True)
    add_pattern(x, eater_C, y_eC, x_eC)

    # ── Right lane ────────────────────────
    y_D, x_D = 0, 101
    gun_t = transform_pattern(gun, rot=0, flip_lr=True, flip_ud=False)
    add_pattern(x, gun_t, y_D, x_D)

    return x

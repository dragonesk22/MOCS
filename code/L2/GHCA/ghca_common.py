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

# library file to implement one iteration of the Greenbeg-Hastings CA

import numpy as np
import itertools
import pathlib
import re


def stepGHCA(grid: np.array, exc: int, N: int):
    """
    iterates the Greenberg-Hastings Cellular automaton for one step

    grid: numpy array containing the corresponding state for each cell
    exc: number of excited states
    N: number of total states
    """
    print(grid)
    print(f"grid shape: {grid.shape}")
    neighbours = np.dstack([
        np.roll(grid, i, axis=j)
        for (i, j) in itertools.product([-1, 1], [0, 1])
    ])
    print(f"neighbours shape: {neighbours.shape}")
    print(neighbours)
    next_grid = np.zeros_like(grid)
    next_grid[grid > 0] = (grid[grid > 0] + 1) % N
    print(next_grid)
    now_excited = np.any(
        (neighbours > 0) & (neighbours <= exc), axis=2) & (grid == 0)
    print(now_excited)
    next_grid[now_excited] = 1
    print(next_grid)
    return next_grid


def random_grid(size: int,
                N: int,
                occupancy: float = 0.2,
                rng=np.random.default_rng()):
    occupied = rng.random(size=(size, size)) < occupancy
    grid = np.zeros((size, size), dtype=np.uint8 if N < 256 else np.int64)
    grid[occupied] = rng.integers(1, N, size=np.sum(occupied))
    return grid


def read_and_parse_grid(file: pathlib.Path, size: int):
    grid = np.zeros((size, size))
    parse_regex = re.compile(r"^\((\d+),(\d+),(\d+)\)$")
    with file.open() as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            print(line)
            try:
                x, y, val = [int(i) for i in parse_regex.match(line).groups()]
            except Exception:
                print(f"can't parse line '{line}', skipping")
            grid[x, y] = val
    return grid


def write_grid_to_file(grid: np.ndarray, file: pathlib.Path):
    with file.open("w") as f:
        for (idx, val) in np.ndenumerate(grid):
            print("(", end='', file=f)
            print(*[*idx, int(val)], sep=",", end=")\n", file=f)

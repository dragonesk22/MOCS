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

from ghca_common import stepGHCA, random_grid, read_and_parse_grid, write_grid_to_file
import numpy as np
import argparse
import pathlib
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import colors
import sys
import os
import glob


def save_sequence(seq_grids, path: pathlib.Path, N: int):
    print(f"saving sequence to {str(path)}", file=sys.stderr)
    if path.is_dir() and path.exists():
        to_delete = glob.glob(str(path) + "*.png")
        for delt in to_delete:
            os.remove(delt)
    else:
        path.mkdir()
    for i in range(len(seq_grids)):
        saveat = path.joinpath(f"{i:04d}.png")
        print(f"saving grid to {saveat}")
        mpl.image.imsave(saveat,
                         np.array(seq_grids[i]),
                         vmin=0,
                         vmax=N,
                         cmap="viridis",
                         dpi=50)


def find_periodic_state(grid: np.array, exc: int, N: int, write_seq=None):
    seen_states = [grid.tolist()]
    while True:
        grid = stepGHCA(grid, exc, N)
        if grid.tolist() in seen_states:
            first_occurred = seen_states.index(grid.tolist())
            print(
                f"found periodic state, transient: {first_occurred} steps,"
                f" period: {len(seen_states)-first_occurred} steps",
                file=sys.stderr)
            if write_seq is not None:
                save_sequence(seen_states[first_occurred:], write_seq, N)
            return grid
        else:
            seen_states.append(grid.tolist())


def main():
    ap = argparse.ArgumentParser(
        description="Retrieves configuration from a file or generates a"
        " random starting configuration, iterates it and saves it to a file.",
        add_help=True,
        suggest_on_error=True)
    ap.add_argument("-s",
                    "--size",
                    default=10,
                    type=int,
                    help="Size of the grid, n x n")
    ap.add_argument("-e",
                    "--excited",
                    default=1,
                    type=int,
                    help="Number of Excited states")
    ap.add_argument("-N",
                    "--num_states",
                    default=3,
                    type=int,
                    help="Total Number of states")
    ap.add_argument("--show",
                    action="store_true",
                    help="Show the result after each step")
    ap.add_argument("--seed",
                    help="Seed for RNG for reproducibility",
                    type=int)
    ap.add_argument("filename", nargs="?", type=pathlib.Path)
    ap.add_argument("-o", "--output", nargs="?", type=pathlib.Path)
    ap.add_argument("--save-image",
                    nargs="?",
                    type=pathlib.Path,
                    help="Path to save graphical version of periodic state as")
    ap.add_argument("--sequence-dir", nargs="?", type=pathlib.Path)
    args = ap.parse_args()

    if args.num_states < 3:
        ap.error("-N must be at least 3")

    if args.excited < 1 or args.num_states < args.excited + 2:
        ap.error("there must be at least one rest state but e + 2 = "
                 f"{args.excited + 2} > {args.num_states} = N")

    if args.seed is not None:
        global rng
        rng = np.random.default_rng(args.seed)

    grid = random_grid(
        args.size,
        args.num_states) if args.filename is None else read_and_parse_grid(
            args.filename, args.size)

    periodic_state = find_periodic_state(grid, args.excited, args.num_states,
                                         args.sequence_dir)
    if args.output is not None:
        write_grid_to_file(periodic_state, args.output)

    if args.show or args.save_image is not None:
        fig, (ax, colorax) = plt.subplots(ncols=2, width_ratios=[20, 1])
        cmap = mpl.colormaps["viridis"].resampled(args.num_states)
        img = ax.imshow(periodic_state, cmap=cmap)
        colornorm = colors.BoundaryNorm(np.arange(-0.5, args.num_states + 0.5),
                                        cmap.N)
        cbar = plt.colorbar(plt.cm.ScalarMappable(norm=colornorm, cmap=cmap),
                            cax=colorax)
        cbar.set_ticks(range(args.num_states))
        plt.tight_layout()
        if args.save_image is not None:
            fig.savefig(args.save_image)
        if args.show:
            plt.show()
        else:
            plt.close(fig)


if __name__ == "__main__":
    main()

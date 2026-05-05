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

from ghca_common import stepGHCA, read_and_parse_grid, random_grid, write_grid_to_file
import numpy as np
import argparse
import pathlib
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import colors
import time

# rng = np.random.default_rng()


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
    ap.add_argument("-n",
                    "--nsteps",
                    default=100,
                    type=int,
                    help="Number of steps to take before saving and exiting")
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
    ap.add_argument("--delay",
                    type=float,
                    help="delay between steps,"
                    " useful in combination with --show",
                    default="0")
    ap.add_argument("filename", nargs="?", type=pathlib.Path)
    ap.add_argument("-o", "--output", nargs="?", type=pathlib.Path)
    ap.add_argument("--save-image",
                    nargs="?",
                    type=pathlib.Path,
                    help="Path to save graphical version of final state as")
    args = ap.parse_args()

    if args.num_states < 3:
        ap.error("-N must be at least 3")

    if args.excited < 1 or args.num_states < args.excited + 2:
        ap.error("there must be at least one rest state but e + 2 = "
                 f"{args.excited + 2} > {args.num_states} = N")

    rng = np.random.default_rng(args.seed)

    grid: np.array = random_grid(
        args.size, args.num_states,
        rng=rng) if args.filename is None else read_and_parse_grid(
            args.filename, args.size)
    grid = grid.astype(np.uint8 if args.num_states < 256 else np.int)

    if args.show or args.save_image is not None:
        fig, (ax, colorax) = plt.subplots(ncols=2, width_ratios=[10, 1])
        fig.suptitle(
            f"GHCA with size {args.size}x{args.size} with $N={args.num_states}$, $e={args.excited}$"
        )
        cmap = mpl.colormaps["viridis"].resampled(args.num_states)
        colornorm = colors.BoundaryNorm(np.arange(-0.5, args.num_states + 0.5),
                                        cmap.N)
        img = ax.imshow(grid, cmap=cmap, norm=colornorm)
        cbar = plt.colorbar(plt.cm.ScalarMappable(norm=colornorm, cmap=cmap),
                            cax=colorax)
        cbar.set_ticks(range(args.num_states))
        fig.canvas.draw()
        plt.tight_layout()
        if args.show:
            plt.show(block=False)

    if args.show:
        img.set_data(grid)
        fig.canvas.draw()
        fig.canvas.flush_events()
    for _ in range(args.nsteps):
        grid = stepGHCA(grid, args.excited, args.num_states)
        if args.show:
            img.set_data(grid)
            fig.canvas.draw()
            fig.canvas.flush_events()
        time.sleep(args.delay)
        if not grid.any():
            break
        #plt.imshow(grid)
        #plt.show()

    if args.output is not None:
        write_grid_to_file(grid, args.output)

    if args.save_image is not None:
        fig.savefig(args.save_image)

    if args.show:
        plt.imshow(grid, cmap="viridis")
        plt.show()


if __name__ == "__main__":
    main()

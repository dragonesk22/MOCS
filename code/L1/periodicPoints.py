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

import sys
import time

from sympy import Matrix, lambdify, simplify
from sympy import symbols as sym
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

try:
    import plotext as plt_
except ImportError:
    plt_ = None

rc('text', usetex=True)
rc('font', family='serif', size=12)




def set_grid_search(a, b, M):
    """
    2D evenly spaced square grid [a,b]^2
    :param a:
    :param b:
    :param M: M^2 points
    :return: x_flat, y_flat, x_grid, y_grid
    """
    grid = np.linspace(a, b, M)
    x_grid, y_grid = np.meshgrid(grid, grid)
    x_flat = x_grid.flatten()
    y_flat = y_grid.flatten()
    return x_flat, y_flat, x_grid, y_grid



def F_p(F, x, y, p):
    F_ = F(x,y)
    for _ in range(p-1):
        u, v = F_[0], F_[1]
        F_ = F(u, v)
    return F_

def G_p(F, x, y, p):
    return F_p(F, x, y, p) - Matrix([x, y])


def newton_raphson(x_0, y_0, G_p_num, J_p_num,
                   max_iter=100,
                   α=1.0,
                   ε_tol=1e-10,
                   save_trajectory=False,
                   pbar=None):

    x_prev = np.array([x_0, y_0], dtype=float)
    x_next = None

    if save_trajectory:
        X = np.zeros((2, max_iter))
        X[:, 0] = x_prev

    for n in range(1, max_iter + 1):

        G_n = G_p_num(x_prev[0], x_prev[1]).flatten()
        J_n = J_p_num(x_prev[0], x_prev[1])

        try:
            h_n = np.linalg.solve(J_n, -G_n)
        except np.linalg.LinAlgError:
            break

        x_next = x_prev + α * h_n

        ε = np.linalg.norm(x_next - x_prev)

        if pbar is not None:
            singularity = np.linalg.cond(J_n)
            pbar.set_postfix(cond_J=f"{singularity:.2e}")


        if save_trajectory:
            X[:, n-1] = x_next

        if ε < ε_tol:
            if save_trajectory:
                return X[:, :n], x_next
            return x_next

        x_prev = x_next

    if save_trajectory:
        return X[:, :max_iter], None

    return None


def valid_root(F, x, p, ε_tol, points_list=None):
    """
    Validate root x to be a truly minimal period root and optionally unique in points_list.
    A point x has minimal period p if F^p(x) = x and F^k(x) != x for all 1 <= k < p.
    """
    if x is None:
        return False

    if not ((0 <= x[0] <= 1) and (0 <= x[1] <= 1)):
        return False

    # Check for uniqueness in the list if provided
    if points_list is not None:
        for q in points_list:
            if np.linalg.norm(x - q) < 1e-7:
                return False

    # Check if it is a fixed point for any k < p (minimal period logic)
    z = x
    for k in range(1, p):
        z = F(z[0], z[1]).flatten()
        if np.linalg.norm(z - x) < ε_tol:
            return False

    # Check if it is a fixed point for k = p
    z = F(z[0], z[1]).flatten()
    if np.linalg.norm(z - x) < ε_tol:
        return True

    return False






def grid_search(F_num, x_coords, y_coords, G_p_num, J_p_num, p, save_trajectories=False, ε_tol=1e-10):
    """
    :param F_num: purely numerical map of F
    :param x_coords: x coordinates (flattened)
    :param y_coords: y coordinates (flattened)
    :param G_p_num: numerical G_p (lambdified)
    :param J_p_num: numerical Jacobian J_p (lambdified)
    :param p: period
    :param save_trajectories:
    :param ε_tol: tolerance for validation
    :return: valid_roots, convergence_mask
    """
    valid_roots = []
    trajectories = [] if save_trajectories else None
    convergence_mask = np.zeros(len(x_coords), dtype=bool)

    # Use tqdm if available
    iterator = zip(x_coords, y_coords)
    if tqdm is not None:
        iterator = tqdm(iterator, total=len(x_coords), desc="Running Gridsearch")

    all_xr = []
    for i, (x0, y0) in enumerate(iterator):
        result = newton_raphson(
            x0, y0,
            G_p_num, J_p_num,
            save_trajectory=save_trajectories,
            ε_tol=ε_tol,
            pbar=iterator if tqdm is not None else None
        )
        if save_trajectories:
            X, x_r = result
        else:
            x_r = result


        is_valid = valid_root(F_num, x_r, p, ε_tol, points_list=None)

        if x_r is not None and is_valid:
            convergence_mask[i] = True
            if save_trajectories:
                trajectories.append(X)
            # Now check for uniqueness to add to valid_roots
            is_unique = True
            for q in valid_roots:
                if np.linalg.norm(x_r - q) < 1e-7:
                    is_unique = False
                    break
            if is_unique:
                valid_roots.append(x_r.copy())
        """
        if plt_ is not None and (i % 100 == 99 or i == len(x_coords) - 1):
            plt_.clf()
            x_proc = x_coords[:i+1]
            y_proc = y_coords[:i+1]
            cv = convergence_mask[:i+1]
            if np.any(cv):
                plt_.scatter(x_proc[cv], y_proc[cv], color="blue")
            fl = ~cv
            if np.any(fl):
                plt_.scatter(x_proc[fl], y_proc[fl], color="red")
            if i+1 < len(x_coords):
                x_pend = x_coords[i+1:]
                y_pend = y_coords[i+1:]
                if len(x_pend) > 1000:
                    step = len(x_pend) // 1000
                    plt_.scatter(x_pend[::step], y_pend[::step], color="green")
                else:
                    plt_.scatter(x_pend, y_pend, color="green")
            plt_.xlim(0, 1)
            plt_.ylim(0, 1)
            plt_.title(f"Grid Search Progress: {i+1}/{len(x_coords)}")
            plt_.show()
            plt_.clear_terminal()
        """


    if save_trajectories:
        return trajectories, valid_roots, convergence_mask

    return valid_roots, convergence_mask

def plot_results(filename, valid_roots, convergence_mask, x_grid, y_grid, p, ε, r1, r2, trajectories=None):
    """
    Plot the results of the grid search using a smooth background for convergence basins.
    """
    plt.figure(figsize=(8, 8))

    # Reshape convergence_mask to grid shape for smooth plotting
    M = x_grid.shape[0]
    convergence_grid = convergence_mask.reshape((M, M))

    # Plot the convergence basin as a smooth background
    plt.imshow(convergence_grid, extent=(0, 1, 0, 1), origin='lower',
               cmap='coolwarm', alpha=0.6, aspect='auto')

    if trajectories:
        for traj in trajectories:
            plt.plot(traj[0, :], traj[1, :], color='black', alpha=0.3, linewidth=0.5)

    # Add a custom legend proxy for the background
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='s', color='w', label='Convergence basin',
               markerfacecolor='red', markersize=10, alpha=0.6),
        Line2D([0], [0], marker='s', color='w', label='No convergence',
               markerfacecolor='blue', markersize=10, alpha=0.6)
    ]

    if len(valid_roots) > 0:
        valid_roots = np.array(valid_roots)
        plt.scatter(valid_roots[:, 0], valid_roots[:, 1],
                    marker='o', facecolors='none', edgecolors='black', s=100, linewidths=1.5,
                    label=f'Distinct period-{p} points')

        plt.scatter(valid_roots[:, 0], valid_roots[:, 1],
                    marker='x', color='black', s=100, linewidths=1.5,
                    label='_nolegend_')

    plt.title(f'Period-{p} points and convergence basins\n'
              f'$\\varepsilon = {ε},\\ r_1 = {r1},\\ r_2 = {r2}$')
    plt.xlabel('$x$')
    plt.ylabel('$y$')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True, linestyle='--', alpha=0.5)

    # Combine existing legend with custom elements
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend(handles=legend_elements + handles, loc='best')

    plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
    plt.axvline(0, color='gray', linestyle='--', linewidth=0.5)
    plt.savefig(f'{filename}.pdf',format='pdf', dpi=100)
    #plt.show()





def main(argv):
    if len(argv) == 6:
        p, ε, r_1, r_2, M = argv[1:]
        p, M = int(p), int(M)
        ε, r_1, r_2 = [float(var) for var in (ε, r_1, r_2)]
    else:
        p, ε, r_1, r_2, M = argv

    x_grid_flat, y_grid_flat, x_grid, y_grid = set_grid_search(0, 1, M)
    save_trajectory = False

    x_, y_, ε_, r_1_, r_2_ = sym('x y ε r_1 r_2')
    F_ = Matrix([
        (1 - ε_) * r_1_ * x_ * (1 - x_) + ε_ * r_2_ * y_ * (1 - y_),
        (1 - ε_) * r_2_ * y_ * (1 - y_) + ε_ * r_1_ * x_ * (1 - x_)
    ])

    F_sym_func = lambdify((x_, y_), F_, 'sympy')
    map_ = {
        ε_: ε,
        r_1_: r_1,
        r_2_: r_2
        }

    Gp_sym = G_p(F_sym_func, x_, y_, p).subs(map_)
    Jp_sym = Gp_sym.jacobian([x_, y_])

    # Pre-lambdify for performance
    Gp_num = lambdify((x_, y_), Gp_sym, 'numpy')
    Jp_num = lambdify((x_, y_), Jp_sym, 'numpy')
    F_num = lambdify((x_, y_), F_.subs(map_), 'numpy')

    result = grid_search(F_num, x_grid_flat, y_grid_flat, Gp_num, Jp_num, p, save_trajectory)
    
    if save_trajectory:
        trajectories, fix_points, convergence_mask = result
    else:
        fix_points, convergence_mask = result
        trajectories = None

    print(f"Found {len(fix_points)} periodic points of minimal period {p}")
    print(f"p = {p}, ε = {ε}, r_1 = {r_1}, r_2 = {r_2}")

    plot_results(f'{p}_{ε}_{r_1}_{r_2}', fix_points, convergence_mask, x_grid, y_grid, p, ε, r_1, r_2, trajectories)
    for point in fix_points:
        print(point)
    print()

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] in ("-h", "--help"):
        print("Usage:")
        print("  python periodicPoints.py p ε r1 r2 M")
        print("or")
        print("  python periodicPoints.py") 
        print("")
        print("Arguments:")
        print("  p        period")
        print("  ε  coupling parameter")
        print("  r_1       logistic parameter 1")
        print("  r_2       logistic parameter 2")
        print("  M        Gridsearch resolution M x-points times M y-points")
        sys.exit(0)

    if len(sys.argv) == 1:

        main([1, 0.3, 3.1, 3.1, 50]) 
        main([1, 0.3, 3.1, 3.4, 50]) 
        main([1, 0.3, 3.1, 3.55, 50])
        main([1, 0.3, 3.1, 3.8, 50])
        
        main([2, 0.3, 3.1, 3.1, 50]) 
        main([2, 0.3, 3.1, 3.4, 50]) 
        main([2, 0.3, 3.1, 3.55, 50])
        main([2, 0.3, 3.1, 3.8, 50])

        main([3, 0.3, 3.1, 3.1, 50]) 
        main([3, 0.3, 3.1, 3.4, 50]) 
        main([3, 0.3, 3.1, 3.55, 50])
        main([3, 0.3, 3.1, 3.8, 50])

        
        main([4, 0.3, 3.1, 3.1, 50]) 
        main([4, 0.3, 3.1, 3.4, 50]) 
        main([4, 0.3, 3.1, 3.55, 50])
        main([4, 0.3, 3.1, 3.8, 50])


    else:
        main(sys.argv)



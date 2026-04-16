import matplotlib.pyplot as plt
from common import coupled_map
import numpy as np

default_params = (3.1, 3.1, 0.3)
default_x0y0 = (0.3, 0.7)


def get_trajectory(x0y0, params, traj_length=100, trans=20):
    """
    get trajectory of the coupled map
    
    start from x0y0 and with parameters `params`, return array of `traj_length`
    after warming up for `trans` steps
    """

    xy = np.array(x0y0).copy()

    def thismap(xy):
        return coupled_map(xy, params)

    for _ in range(trans):
        xy = thismap(xy)
    traj = np.zeros((traj_length, 2))
    for i in range(traj_length):
        xy = thismap(xy)
        traj[i] = xy
    return traj


def plot_phase_portrait(x0y0,
                        params,
                        traj_length=200,
                        trans=20,
                        should_print=False):
    traj = get_trajectory(x0y0, params, traj_length, trans)
    if should_print:
        print(traj[-1])
    plt.scatter(
        *traj.T,
        c=np.array(range(traj_length)),
        label=
        f"x0y0=({x0y0[0]:.3f}, {x0y0[1]:.3f}), (r1,r2,$\\epsilon$)={params}")


def get_report_figures():
    trans_val = 30
    plt.close()
    for param in [(2.8, 2.9, 0.1), (3.1, 3.4, 0.3), (3.85, 3.95, 0.2)]:
        plot_phase_portrait(np.random.rand(2), param, trans=trans_val)
        plot_phase_portrait(np.random.rand(2), param, trans=trans_val)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.suptitle(f"Phase Portrait for (r1, r2, $\\epsilon$)={param}")
        plt.colorbar(label="Step")
        plt.savefig(f"figures/phase_{param}.pdf")
        plt.close()


if __name__ == "__main__":
    trans_val = 20
    plot_phase_portrait(np.random.rand(2), default_params, trans=trans_val)
    plot_phase_portrait(np.random.rand(2), default_params, trans=trans_val)
    plt.legend()
    plt.colorbar()
    plt.show()
    get_report_figures()

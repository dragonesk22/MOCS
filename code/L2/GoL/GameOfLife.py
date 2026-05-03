import numpy as np
from scipy.ndimage import convolve
import matplotlib.pyplot as plt
from matplotlib import rc
from GoLogic import AND, OR, NOT
rc('text', usetex=True)
rc('font', family='serif', size=12)

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

def F(X, K=np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
], dtype=np.uint8)):

    N = convolve(X, K, mode="constant", cval=0)
    return ((N == 3) | ((X == 1) & (N == 2))).astype(np.uint8)


n = 400
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

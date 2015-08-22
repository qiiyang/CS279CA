import random as rnd

import numpy as np
import matplotlib.pyplot as plt


def diff(x, D, t):
    y = 1. / t**0.5 / np.exp(x*x / 4 / D / (t**2))
    return y

if __name__ == '__main__':
    
    rnd.seed()
    
    N = 300
    L = 300.
    dx = L / N
    xs = np.arange(-L/2., L/2.+dx, dx)
    
    plt.xlabel("x")
    plt.ylabel("concentration")
    
    plt.plot(xs, diff(xs, 50., 1.), "r-", label="t=1")
    plt.plot(xs, diff(xs, 50., 2.), "g-", label="t=2")
    plt.plot(xs, diff(xs, 50., 3.), "b-", label="t=3")
    plt.plot(xs, diff(xs, 50., 10.), "k-", label="t=10")
    plt.legend()
    
    plt.show()


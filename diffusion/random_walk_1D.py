import random as rnd

import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    
    rnd.seed()
    
    N = 300
    ts = np.arange(N)
    xs = np.empty(N)
    
    plt.xlabel("time (s)")
    plt.ylabel("position")
    
    v = 0.
    for t in ts:
        xs[t] = v
        v = v + 2. * rnd.randint(0,1) - 1.
    plt.plot(ts, xs, "r-")
    
    v = 0.
    for t in ts:
        xs[t] = v
        v = v + 2. * rnd.randint(0,1) - 1.
    plt.plot(ts, xs, "g-")
    
    v = 0.
    for t in ts:
        xs[t] = v
        v = v + 2. * rnd.randint(0,1) - 1.
    plt.plot(ts, xs, "b-")
    
    v = 0.
    for t in ts:
        xs[t] = v
        v = v + 2. * rnd.randint(0,1) - 1.
    plt.plot(ts, xs, "k-")
    
    v = 0.
    for t in ts:
        xs[t] = v
        v = v + 2. * rnd.randint(0,1) - 1.
    plt.plot(ts, xs, "y-")
    
    v = 0.
    for t in ts:
        xs[t] = v
        v = v + 2. * rnd.randint(0,1) - 1.
    plt.plot(ts, xs, "c-")
    
    v = 0.
    for t in ts:
        xs[t] = v
        v = v + 2. * rnd.randint(0,1) - 1.
    plt.plot(ts, xs, "m-")
    

    
    plt.show()


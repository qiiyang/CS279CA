import numpy as np
import matplotlib.pyplot as plt

# CONSTANTS
HALF_RANGE = 5000    # Will use array[HALF_RANGE] as x=0, therefore arraysize = 2 * HALF_RANGE - 1
PLOT_LIM = 500    # only plot between +/- this value, in order to remove the boundary effect

def two_steps(width=200):
    a = np.zeros(2*HALF_RANGE - 1)
    for i in range(width):
        a[HALF_RANGE + i] = 1.
        a[HALF_RANGE - i - 1] = 2.
    return a
 
def gaussian(sigma=100):
    a = 1. / sigma / (np.pi * 2)**0.5 * np.exp((np.arange(2*HALF_RANGE - 1) - HALF_RANGE)**2 / -2. / sigma**2)
    return a

    
def plot_f(f, fmt="b-", ylabel="y", title="", xlim=PLOT_LIM, ylims=None):
    plt.xlabel("x")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xlim(-xlim, xlim)
    if ylims != None:
        plt.ylim(ylims[0], ylims[1])
    xs = np.arange(HALF_RANGE * 2 - 1) - HALF_RANGE
    plt.plot(xs, f, fmt)
    plt.show()
    
def plot_convolution(f, g, fmt="b-", ylabel="y", title="", xlim=PLOT_LIM, ylims=None):
    conv = np.convolve(f, g, "full")
    plt.xlabel("x")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xlim(-xlim, xlim)
    if ylims != None:
        plt.ylim(ylims[0], ylims[1])
    xs = np.arange(HALF_RANGE * 4 - 3) - HALF_RANGE * 2 - 1    
    plt.plot(xs, conv, fmt)
    plt.show()
    
if __name__ == '__main__':
    plot_f(two_steps(), fmt="b-", ylims=(-0.3, 2.3))
    plot_f(gaussian(sigma=20.))
    plot_convolution(two_steps(), gaussian(20.), ylims=(-0.3, 2.3))
    
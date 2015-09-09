from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt

# CONSTANTS
HALF_RANGE = 500    # Will use array[HALF_RANGE] as x=0, therefore arraysize = 2 * HALF_RANGE - 1
PLOT_LIM = 100    # only plot between +/- this value, in order to remove the boundary effect

def gaussian_kernel(std):
    a = np.empty([2 * HALF_RANGE - 1, 2 * HALF_RANGE - 1])
    for i in range(2 * HALF_RANGE - 1):
        for j in range(2 * HALF_RANGE - 1):
            a[i,j] = 1. / std**2 / np.pi / 2. * np.exp(((i - HALF_RANGE)**2 + (j - HALF_RANGE)**2) / -2. / std**2)
    return a

def plot_2d(fs, title="", xlim=PLOT_LIM):
    x = np.arange(2 * HALF_RANGE - 1) - HALF_RANGE
    xs, ys = np.meshgrid(x,x)    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    implot = ax.pcolormesh(xs, ys,fs)
    implot.set_cmap('Greys')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)
    plt.xlim(-xlim, xlim)
    plt.ylim(-xlim, xlim)
    fig.colorbar(implot)
    plt.show()
    
if __name__ == '__main__':
    original = plt.imread("cross.png")
    #plot_2d(original, "f(x,y)")
    gaus = gaussian_kernel(10.)
    #plot_2d(gaus, "g(x,y)")
    conv = ndimage.gaussian_filter(original, sigma=10.)
    plot_2d(conv, "f convolves with g")
    
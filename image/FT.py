import random
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt

N = 1000
PLOT_LIM = 100    # only plot between +/- this value, in order to remove the boundary effect

X = np.fft.fftfreq(N, d=1./N) # The x coordinates
K = np.fft.fftfreq(N)
XS, YS = np.meshgrid(X,X) # The 2D real coordinates
KX, KY = np.meshgrid(K,K) # The 2D frequency coordinates.
    
def gaussian(std):
    a = np.empty([N, N])
    for i in range(N):
        for j in range(N):
            a[i,j] = 1. / std**2 / np.pi / 2. * np.exp((X[i]**2 + X[j]**2) / -2. / std**2)
    return a
    
def window(odd_size):
    m = (odd_size - 1) // 2
    v = 1. / odd_size**2
    a = np.empty([N, N])
    for i in range(-m, m+1):
        for j in range(-m, m+1):
            a[i,j] = v
    return a
    
def plot_2d(xs, ys, fs, title="", xlabel="x", ylabel="y", xlim=PLOT_LIM):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    implot = ax.pcolormesh(xs, ys, fs)
    implot.set_cmap('Greys')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.xlim(-xlim, xlim)
    plt.ylim(-xlim, xlim)
    fig.colorbar(implot)
    plt.show()
    
if __name__ == '__main__':
    gaus = gaussian(3.)
    plot_2d(np.fft.fftshift(XS), np.fft.fftshift(YS), np.fft.fftshift(gaus), xlim=30)
    gaus_ft = np.fft.fft2(gaus)
    #plot_2d(np.fft.fftshift(KX), np.fft.fftshift(KY), np.fft.fftshift(gaus_ft), xlabel="spacial frequency k_x", ylabel="spacial frequency k_y", xlim=0.5)
    
    wind = window(5)
    #plot_2d(np.fft.fftshift(XS), np.fft.fftshift(YS), np.fft.fftshift(wind), xlim=30)
    wind_ft = np.fft.fft2(wind)
    #plot_2d(np.fft.fftshift(KX), np.fft.fftshift(KY), np.fft.fftshift(wind_ft), xlabel="spacial frequency k_x", ylabel="spacial frequency k_y", xlim=0.5)
    
    
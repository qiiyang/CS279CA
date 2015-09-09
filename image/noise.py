import random
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt

def plain_img(shape, value):
    fs = np.full(shape, value)
    return fs

def add_gaussian_noise(img, std):
    a = img.copy()
    for x in range(a.shape[0]):
        for y in range(a.shape[1]):
            a[x,y] += random.gauss(0, std)
    return a
    
def add_saltpepper_noise(img, prob, extremals=[0., 1.]):
    a = img.copy()
    for x in range(a.shape[0]):
        for y in range(a.shape[1]):
            r = random.uniform(0,1)
            if r < prob:
                a[x,y] = random.choice(extremals)
    return a

def plot_img(img, vmin=0, vmax=1.):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    implot = ax.imshow(img, origin='lower', interpolation="none", vmin=vmin, vmax=vmax)
    implot.set_cmap('Greys')
    ax.set_xlabel("pixels")
    ax.set_ylabel("pixels")
    fig.colorbar(implot)
    plt.show()
    
def ex1():
    plain = plain_img((20,20), 0.5)
    plot_img(plain)
    plain_gauss = add_gaussian_noise(plain, 0.1)
    plot_img(plain_gauss)
    plain_salt = add_saltpepper_noise(plain, 0.05)
    plot_img(plain_salt)
    
def ex2gauss():
    test = plt.imread("2.test.png")
    plot_img(test)
    test_gauss = add_gaussian_noise(test, 0.1)
    plot_img(test_gauss)
    test_gauss = ndimage.gaussian_filter(test_gauss, 1)
    plot_img(test_gauss)
    
if __name__ == '__main__':
    random.seed()
    #ex1()
    ex2()
    
    
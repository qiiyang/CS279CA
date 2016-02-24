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

def plot_img(img, vmin=None, vmax=None):
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
    test = plt.imread("test.png")
    plot_img(test)
    test_noise = add_gaussian_noise(test, 0.1)
    plot_img(test_noise)
    t1 = ndimage.uniform_filter(test_noise, size=3)
    plot_img(t1)
    t1 = ndimage.gaussian_filter(test_noise, sigma=1)
    plot_img(t1)
    t1 = ndimage.median_filter(test_noise, size=3)
    plot_img(t1)
    
    
def ex2salt():
    test = plt.imread("test.png")
    plot_img(test)
    test_noise = add_saltpepper_noise(test, 0.05)
    plot_img(test_noise)
    t1 = ndimage.uniform_filter(test_noise, size=3)
    plot_img(t1)
    t1 = ndimage.gaussian_filter(test_noise, sigma=1)
    plot_img(t1)
    t1 = ndimage.median_filter(test_noise, size=3)
    plot_img(t1)
    
def ex2edge():
    test = plt.imread("test.png")
    plot_img(test)
    gaus = ndimage.gaussian_filter(test, sigma=2)
    plot_img(gaus)
    t1 = test - gaus
    plot_img(t1)
    
    
if __name__ == '__main__':
    random.seed(20150909)
    #ex1()
    #ex2gauss()
    #ex2salt()
    ex2edge()
    
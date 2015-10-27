import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plane_wave(kx, ky, N): 
    # return three 2D arrays (xs, ys, fs) where xs, ys are the coordinates and fs is the wave form
    # N: steps per dimension; step size always = 1
    xs = np.empty([N, N])
    ys = np.empty([N, N])
    fs = np.empty([N, N])
    for x in range(N):
        for y in range(N):
            xs[x, y] = x
            ys[x, y] = y
            fs[x, y] = np.cos(2.*np.pi*kx*x + 2.*np.pi*ky*y)
    return (xs, ys, fs)
    
def wireframe(kx, ky, N, rstride=1, cstride=1):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    (xs, ys, fs) = plane_wave(kx, ky, N)
    ax.plot_wireframe(X=xs, Y=ys, Z=fs, rstride=rstride, cstride=cstride)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("f(x,y)")
    plt.show()
    
def surface(kx, ky, N, rstride=1, cstride=1, color='b'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    (xs, ys, fs) = plane_wave(kx, ky, N)
    ax.plot_surface(X=xs, Y=ys, Z=fs, rstride=rstride, cstride=cstride, color=color)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("f(x,y)")
    plt.show()
    
def colormap(kx, ky, N, cmap='Greys'):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    (xs, ys, fs) = plane_wave(kx, ky, N)
    implot = ax.imshow(fs, origin='lower')
    implot.set_cmap(cmap)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    fig.colorbar(implot)
    plt.show()
    

if __name__ == '__main__':
    #wireframe(0.01, 0.02, 200, rstride=10, cstride=10)
    #surface(0.01, 0.02, 200, rstride=10, cstride=10)
    colormap(0.01, 0.02, 200)
    



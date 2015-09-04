import numpy as np
import matplotlib.pyplot as plt

# CONSTANTS
HALF_RANGE = 5000    # Will use array[HALF_RANGE] as x=0, therefore arraysize = 2 * HALF_RANGE
HALF_WINDOW = 500    # only plot between +/- this value, in order to remove the boundary effect

def two_steps():
    a = np.zeros(2*HALF_RANGE)
    for i in range(200):
        a[HALF_RANGE + i] = 1.
        a[HALF_RANGE - i - 1] = 2.
    return a
    

    
def plot_f(f, style="dots", ylabel="y", title="", xlim=50.):
    plt.xlabel("x")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xlim(-xlim, xlim)
    xs = np.arange(1000) - 500.
    if style == "dots":
        plt.plot(xs, f, "b.")
    elif style == "stem":
        plt.stem(xs, f, markerfmt="bo", linefmt="b--", basefmt="k-")
    plt.show()
    
def plot_overlap():
    f = two_spikes()
    g = cone()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("g(x) spreading around each pixels of f(x)")
    plt.xlim(-50, 50)
    xs = np.arange(1000) - 500.
    plt.plot(xs-20., g, "b.")
    plt.plot(xs+20., 2*g, "b.")
    plt.stem(xs, f, markerfmt="ro", linefmt="r--", basefmt="k-")
    plt.show()
    
def plot_convolution(f, g):
    g = cone()
    conv = np.zeros(1000)
    for i in range(-50, 50):
        conv[500+i] = 2. * g[500+i - 20] + g[500+i + 20]

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("g(x) convolves with f(x)")
    plt.xlim(-50, 50)
    xs = np.arange(1000) - 500.
    plt.plot(xs, conv, "b.")
    plt.show()
    
if __name__ == '__main__':
    #plot_f(two_spikes(), style="stem", title="f(x)")  # Plot the two spikes
    #plot_f(cone(), title="g(x)")   # Plot the cone
    #plot_overlap()
    #plot_convolution()
    
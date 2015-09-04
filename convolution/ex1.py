import numpy as np
import matplotlib.pyplot as plt


def two_spikes():
    a = np.zeros(1000)
    a[500-20] = 1.
    a[500+20] = 2.
    return a
    
def cone():
    a = np.zeros(1000)
    for i in range(0, 20):
        a[500-i] = (20. - i) / 20.
    for i in range(0, 30):
        a[500+i] = np.cos(i / 60. * np.pi)
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
    
def plot_convolution():
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
    plot_convolution()
    
import random as rnd

import matplotlib.pyplot as plt
import matplotlib.animation as animation

class RWLatticeOnScreen:
    def __init__(self):
        rnd.seed()
        self.config()
        self.fig, self.ax = plt.subplots()
        self.lines = self.ax.plot([], [], "b-", [],[], "r.")
        self.lines[0].set_linewidth(2)
        self.lines[1].set_markersize(10)
        self.xdata = []
        self.ydata = []
        if self.size == 0:
            self.lim = self.initial_size / 2.
        else:
            self.lim = self.size / 2.
        self.ax.set_ylim(-self.lim, self.lim)
        self.ax.set_xlim(-self.lim, self.lim)  
        self.ax.set_title("0 step")
    
    def config(self, interval=10., size=0, initial_size=40):
        self.interval = interval    # interval between steps in ms
        self.size = size    # positive size for periodic boundries. 0 if infinite   
        self.initial_size = initial_size    # the initial size of the box, ignored for non-zero size
                
    def xy_gen(self):
        self.x = 0
        self.y = 0
        self.t = 0
        yield (0, 0, 0)
        while True:
            self.t += 1
            r1 = rnd.randint(0,1)
            r2 = rnd.choice([-1,1])
            self.x += r1 * r2
            self.y += (1 - r1) * r2 
            yield (self.x, self.y, self.t)
            
    def check_boundary(self):
        if self.size == 0:  # Infinite case, increase boundary
            if (abs(self.x) >= self.lim) or (abs(self.y) >= self.lim):
                self.lim *= 1.5
                self.ax.set_ylim(-self.lim, self.lim)
                self.ax.set_xlim(-self.lim, self.lim)
        else:
            self.x = int((self.x + self.lim) % self.size - self.lim)
            self.y = int((self.y + self.lim) % self.size - self.lim)
                
    
    def update(self, xyt):
        (x, y, t) = xyt
        #print(x,y)
        self.xdata.append(x)
        self.ydata.append(y)
        self.ax.set_title("{0} steps".format(t))
        self.check_boundary()
        self.fig.canvas.draw()
        self.lines[0].set_data(self.xdata, self.ydata)
        self.lines[1].set_data([x], [y])
        return self.lines
        
    def start(self):
        ani = animation.FuncAnimation(self.fig, func=self.update, frames=self.xy_gen, blit=True, interval=self.interval, repeat=False)
        plt.show()
        


if __name__ == '__main__':
    rw = RWLatticeOnScreen()
    rw.start()


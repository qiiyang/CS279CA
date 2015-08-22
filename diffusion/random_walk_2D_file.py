import random as rnd

import matplotlib.pyplot as plt
import matplotlib.animation as animation

class RWLatticeToFile:
    def __init__(self):
        rnd.seed()
        self.fig, self.ax = plt.subplots()
        self.lines = self.ax.plot([], [], "b-", [],[], "r.")
        self.lines[0].set_linewidth(2)
        self.lines[1].set_markersize(10)
        self.xdata = []
        self.ydata = []
        self.t = -2
        self.config()
        self.ax.set_title("0 step")
    
    def config(self, filename="random_walk.mp4", dpi=300, fps=20, frames=1000, step_per_frame=5, size=0, initial_size=40):
        self.size = size    # positive size for reflective boundries. 0 if infinite   
        self.initial_size = initial_size    # the initial size of the box, ignored for non-zero size
        self.filename = filename
        self.frames=frames
        self.dpi = dpi
        self.fps = fps
        self.step_per_frame = step_per_frame
        if self.size == 0:
            self.lim = self.initial_size / 2.
        else:
            self.lim = self.size // 2
        self.ax.set_ylim(-self.lim, self.lim)
        self.ax.set_xlim(-self.lim, self.lim)  
        self.fig.canvas.draw()
                
    def xy_gen(self):
        self.t += 1
        r1 = rnd.randint(0,1)
        r2 = rnd.choice([-1,1])
        self.x += r1 * r2
        self.y += (1 - r1) * r2 
        return (self.x, self.y, self.t)
        
            
    def check_boundary(self):
        if self.size == 0:  # Infinite case, increase boundary
            if (abs(self.x) >= self.lim) or (abs(self.y) >= self.lim):
                self.lim *= 1.5
                self.ax.set_ylim(-self.lim, self.lim)
                self.ax.set_xlim(-self.lim, self.lim)
        else:
            if self.x > self.lim:
                self.x -= 1
            elif self.x < -self.lim:
                self.x += 1
            elif self.y > self.lim:
                self.y -= 1
            elif self.y < -self.lim:
                self.y += 1
     
    def init_frame(self):
        self.x = 0
        self.y = 0
        self.xdata=[0]
        self.ydata=[0]
        self.ax.set_title("{0} steps".format(0))
        self.fig.canvas.draw()
        self.lines[0].set_data([0], [0])
        self.lines[1].set_data([0], [0])
        return self.lines
    
    def update(self, arg):
        if self.t < 0:
            self.t += 1
            return self.init_frame()
        else:
            for i in range(self.step_per_frame):
                (x, y, t) = self.xy_gen()
                #print(x,y)
                self.xdata.append(x)
                self.ydata.append(y)
                self.check_boundary()
            self.ax.set_title("{0} steps".format(t))
            self.fig.canvas.draw()
            self.lines[0].set_data(self.xdata, self.ydata)
            self.lines[1].set_data([x], [y])
            return self.lines
        
    def start(self):
        ani = animation.FuncAnimation(self.fig, func=self.update, frames=self.frames, blit=True, repeat=False)
        ani.save(self.filename, writer='ffmpeg', dpi=self.dpi, fps=self.fps)
        


if __name__ == '__main__':
    rw = RWLatticeToFile()
    rw.config(step_per_frame=1, fps=60, size=80, frames=1200)
    rw.start()


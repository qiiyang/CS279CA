import random as rnd

import matplotlib.pyplot as plt
import matplotlib.animation as animation

class RWLatticeToFile:
    def __init__(self):
        rnd.seed()
        self.config()
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], lw=2)
    
    def config(self, filename="random_walk.mp4", dpi=300, fps=20, frames=1000, step_per_frame=5, size=0, initial_size=40):
        self.size = size    # positive size for periodic boundries. 0 if infinite   
        self.initial_size = initial_size    # the initial size of the box, ignored for non-zero size
        self.filename = filename
        self.frames=frames
        self.dpi = dpi
        self.fps = fps
        self.step_per_frame = step_per_frame
        
    def init_frame(self):
        self.x = 0
        self.y = 0
        self.t = 0
        self.xdata = [0]
        self.ydata = [0]
        self.line.set_data(self.xdata, self.ydata)
        if self.size == 0:
            self.lim = self.initial_size / 2.
        else:
            self.lim = self.size / 2.
        self.ax.set_ylim(-self.lim, self.lim)
        self.ax.set_xlim(-self.lim, self.lim)  
        self.ax.set_title("0 step")
        return self.line,
        
    def xy_gen(self):
        self.t += 1
        r1 = rnd.randint(0,1)
        r2 = rnd.choice([-1,1])
        self.x += r1 * r2
        self.y += (1 - r1) * r2 
        self.ax.set_title("{0} steps".format(self.t))
        self.check_boundary()
        return (self.x, self.y)
            
    def check_boundary(self):
        if self.size == 0:  # Infinite case, increase boundary
            if (abs(self.x) >= self.lim) or (abs(self.y) >= self.lim):
                self.lim *= 1.5
                self.ax.set_ylim(-self.lim, self.lim)
                self.ax.set_xlim(-self.lim, self.lim)
        else:
            self.x = int((self.x + self.lim) % self.size - self.lim)
            self.y = int((self.y + self.lim) % self.size - self.lim)
                
    
    def update(self, arg):
        for i in range(self.step_per_frame):
            (x, y) = self.xy_gen()
            #print(x,y)
            self.xdata.append(x)
            self.ydata.append(y)
        self.line.set_data(self.xdata, self.ydata)
        self.fig.canvas.draw()
        return self.line,
        
    def start(self):
        ani = animation.FuncAnimation(self.fig, func=self.update, frames=self.frames, init_func=self.init_frame, blit=True, repeat=False)
        ani.save(self.filename, writer='ffmpeg', dpi=self.dpi, fps=self.fps)
        


if __name__ == '__main__':
    rw = RWLatticeToFile()
    rw.config(initial_size=80)
    rw.start()


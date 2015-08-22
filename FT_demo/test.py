import math
import numpy as np

import tkinter as tk
from tkinter import ttk, tix, filedialog, font

import matplotlib
matplotlib.use("TkAgg")
matplotlib.rcParams.update({'figure.autolayout': True})
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


class FigureFrame:
    def __init__(self, frame):
        f = Figure(figsize=(4,3), dpi=100)
        a = f.add_subplot(111)
        
        canvas = FigureCanvasTkAgg(f, frame)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.figure = a
        self.canvas = canvas
        self.frame = frame
        
class FTDemo:
    def __init__(self):
        
        #labelFont = font.Font(size=12, weight='bold')
        
        self.root = tk.Tk()
        self.root.title("Fourier Transform Demo")
        
#        self.ybar = ttk.Scrollbar(self.root, orient=tk.VERTICAL)
#        self.ybar.pack(side=tk.RIGHT, fill=tk.Y, expand=tk.YES) 
        
        self.xbar = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        self.xbar.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.YES)
        
        self.mainCanvas = tk.Canvas(self.root, height=100, width=100, background='white')
        
        self.mf = ttk.Frame(self.mainCanvas, padding="3 3 12 12")
        self.mainCanvas.create_window((0,0), window=self.mf)
        
        label=ttk.Label(self.mf, text=">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        label.pack(side=tk.RIGHT)
        
        label=ttk.Label(self.mf, text="test\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|")
        label.pack(side=tk.LEFT)
 

        #self.mainCanvas.config(scrollregion = (0, 0, self.root.winfo_reqwidth(), self.root.winfo_reqheight()))
        self.mainCanvas.config(scrollregion = (0, 0, 10000, 10000))
#        self.ybar.config(command=self.mainCanvas.yview)
        self.xbar.config(command=self.mainCanvas.xview)
        self.mainCanvas.config(xscrollcommand=self.xbar.set)
        #self.mainCanvas.config(yscrollcommand=self.ybar.set)

        self.mainCanvas.pack(side=tk.LEFT) 

        
    def __del__(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent Fatal Python Error: PyEval_RestoreThread: NULL tstate      
        
        
    def start(self):
        tk.mainloop()
 
    
    def load(self):
        self.filename = filedialog.askopenfilename()
        self.fx = np.loadtxt(self.filename)
        n = self.fx.shape[-1]
        if n % 2 == 0:
            n = n - 1
            self.fx = self.fx[0:n]
        
        self.size = n
        self.fk = np.fft.fft(self.fx)
        
        self.N = n // 2
        self.xs = np.arange(self.fx.shape[-1]) - self.N
        self.ks = np.fft.fftfreq(self.fx.shape[-1])
        
        self.fxframe.figure.clear()
        self.fxframe.figure.plot(self.xs, self.fx, "b-")
        self.fxframe.figure.set_xlabel("x")
        self.fxframe.figure.set_ylabel("f(x)")
        self.fxframe.canvas.show()
        
        self.fkframe.figure.clear()
        self.fkframe.figure.plot(self.ks, self.fk.real, "r-", label="Re")
        self.fkframe.figure.plot(self.ks, self.fk.imag, "g-", label="Im")
        self.fkframe.figure.set_xlabel("k")
        self.fkframe.figure.set_ylabel("c(k)")
        self.fkframe.figure.legend()
        self.fkframe.canvas.show()
        
        self.fkframe2.figure.clear()
        self.fkframe2.canvas.show()
        
        self.fxframe2.figure.clear()
        self.fxframe2.canvas.show()
        
        self.slider_sum_to.state(["!disabled"])
        self.slider_sum_to.config(to=self.N, value=1.)
        self.sum_to = 0
        self.k = 0.
        self.label_sum_to.config(text="1          ")
        
        self.button_show_ift.state(["!disabled"])
        self.button_show_singlek.config(text="show |k|=0")
        self.button_show_singlek.state(["!disabled"])
        self.button_save.state(["!disabled"])
        
    def update_sum_to(self, value):
        self.sum_to = int(self.slider_sum_to.get())
        self.k = self.ks[self.sum_to]
        self.button_show_singlek.config(text="show |k|={0:.2}".format(self.k))
        k1 = self.ks[self.sum_to + 1]
        k2 = self.ks[self.size-self.sum_to-1]
        self.label_sum_to.config(text="{0}     ({1:+.2} < k < {2:+.2})          ".format(2 * self.sum_to + 1, k2, k1))
        
    def update(self):
        self.fk2 = self.fk.copy()
        for i in range(self.sum_to + 1, self.size-self.sum_to):
            self.fk2[i] = 0.
        self.fx2 = np.fft.ifft(self.fk2).real
        if self.sum_to == 0:
            self.singlek = self.xs*0. + 1./self.size * self.fk[0]
        else:
            self.singlek = 1./self.size * (self.fk[self.sum_to] * np.exp(2.j*np.pi*self.k*np.arange(self.size)) + self.fk[self.size - self.sum_to] * np.exp(-2.j*np.pi*self.k*np.arange(self.size)))
    
    def show_ift(self):
        self.update()
        self.fxframe2.figure.clear()
        self.fxframe2.figure.plot(self.xs, self.fx2, "b-")
        self.fxframe2.figure.set_xlabel("x")
        self.fxframe2.figure.set_ylabel("f(x)")
        self.fxframe2.canvas.show()
        
        self.fkframe2.figure.clear()
        self.fkframe2.figure.plot(self.ks, self.fk2.real, "r-", label="Re")
        self.fkframe2.figure.plot(self.ks, self.fk2.imag, "g-", label="Im")
        self.fkframe2.figure.set_xlabel("k")
        self.fkframe2.figure.set_ylabel("c(k)")
        self.fkframe2.figure.legend()
        self.fkframe2.canvas.show()
        
    def show_singlek(self):
        self.update()
        self.fxframe2.figure.clear()
        self.fxframe2.figure.plot(self.xs, self.singlek.real, "b-")
        self.fxframe2.figure.set_xlabel("x")
        self.fxframe2.figure.set_ylabel("f(x)")
        self.fxframe2.figure.set_title("f(x, |k|={0:.2})".format(self.k))
        self.fxframe2.canvas.show()
        
        self.fkframe2.figure.clear()
        self.fkframe2.canvas.show()
    

    def save_data(self):
        self.update()
        fns = self.filename.rpartition(".")
        
        fn = "".join([fns[0], "_n={}.".format(self.sum_to), fns[2]])
        np.savetxt(fn, self.fx2)
    
        fn = "".join([fns[0], "_n={}_single_k.".format(self.sum_to), fns[2]])
        np.savetxt(fn, self.singlek)
        
        fn = "".join([fns[0], "_n={}_ft.".format(self.sum_to), fns[2]])
        np.savetxt(fn, self.fk2)
    
    
if __name__ == '__main__':
    #test()
    demo = FTDemo()
    demo.start()
    
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
    def __init__(self, master):
        frame = ttk.Frame(master)
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
        
        self.ybar = ttk.Scrollbar(self.root, orient=tk.VERTICAL)
        self.ybar.pack(side=tk.RIGHT, fill=tk.Y, expand=tk.YES) 
        
        self.xbar = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        self.xbar.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.YES)
        
        self.mainCanvas = tk.Canvas(self.root)
        self.mainCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES) 
        
        self.mainframe = ttk.Frame(self.mainCanvas)
        #self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        #self.mainframe.columnconfigure(0, weight=1)
        #self.mainframe.rowconfigure(0, weight=1)
        self.mainCanvas.create_window((0, 0), window=self.mainframe, anchor=tk.NW)
        
        self.frame1 = ttk.Frame(self.mainframe)
        self.frame1.pack(side=tk.TOP, fill=tk.X)
        
        self.frame2 = ttk.Frame(self.mainframe)
        self.frame2.pack(side=tk.TOP, fill=tk.X)        
        
        self.button_load = ttk.Button(self.frame1, text="load function", command=self.load)
        self.button_load.pack(side=tk.LEFT, padx=30)
        
        label = ttk.Label(self.frame1, text="# of components to use:")
        label.pack(side=tk.LEFT)
        
        self.slider_sum_to = ttk.Scale(self.frame1, orient=tk.HORIZONTAL, length=200, from_=0.0, to=100.0, command=self.update_sum_to)
        self.slider_sum_to.state(["disabled"])
        self.slider_sum_to.pack(side=tk.LEFT)
        
        self.label_sum_to = ttk.Label(self.frame1, text="0          ")
        self.label_sum_to.pack(side=tk.LEFT)
        
        self.button_show_ift = ttk.Button(self.frame1, text="show inverse FT", command=self.show_ift, state=tk.DISABLED)
        self.button_show_ift.pack(side=tk.LEFT, padx=0)  
        
        self.button_show_singlek = ttk.Button(self.frame1, text="show single frequency", command=self.show_singlek, state=tk.DISABLED)
        self.button_show_singlek.pack(side=tk.LEFT, padx=0) 

        self.button_save = ttk.Button(self.frame2, text="save data", command=self.save_data, state=tk.DISABLED)
        self.button_save.pack(side=tk.RIGHT, padx=30)    
        
        self.graphframe = ttk.Frame(self.mainframe)
        self.graphframe.pack(side=tk.TOP, fill=tk.X) 
        
        self.fxLabel = ttk.LabelFrame(self.graphframe, text="Original Function")
        self.fxLabel.grid(column=1, row=1)
        self.fxframe = FigureFrame(self.fxLabel)
        self.fxframe.frame.pack()
        
        self.fkLabel = ttk.LabelFrame(self.graphframe, text="Fourier Transform")
        self.fkLabel.grid(column=2, row=1)
        self.fkframe = FigureFrame(self.fkLabel)
        self.fkframe.frame.pack()
        
        self.fkLabel2 = ttk.LabelFrame(self.graphframe, text="Fourier Components to Use for Reconstruction")
        self.fkLabel2.grid(column=1, row=2)
        self.fkframe2 = FigureFrame(self.fkLabel2)
        self.fkframe2.frame.pack()
        
        self.fxLabel2 = ttk.LabelFrame(self.graphframe, text="Reconstructed Function")
        self.fxLabel2.grid(column=2, row=2)
        self.fxframe2 = FigureFrame(self.fxLabel2)
        self.fxframe2.frame.pack() 

        self.mainCanvas.config(width=self.mainframe.winfo_reqwidth(), height=self.mainframe.winfo_reqheight(), scrollregion = (0, 0, self.mainframe.winfo_reqwidth(), self.mainframe.winfo_reqheight()))
        #self.mainCanvas.config(scrollregion = (0, 0, 10000, 10000))
        self.ybar.config(command=self.mainCanvas.yview)
        self.xbar.config(command=self.mainCanvas.xview)
        self.mainCanvas.config(xscrollcommand=self.xbar.set, yscrollcommand=self.ybar.set)

        
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
        self.xs = np.arange(self.size)
        self.xs_oversampled = np.arange(self.size*10)/10. # oversampled x's
        self.ks = np.fft.fftfreq(self.fx.shape[-1])
        self.korder = [x % n for x in (self.xs - self.N)]   # the order to plot k-components
        #print(self.korder)
        
        ymax = np.nanmax(self.fx)
        ymin = np.nanmin(self.fx)
        self.y1 = ymin - 0.1 * (ymax-ymin)
        self.y2 = ymax + 0.1 * (ymax-ymin)
        
        self.fxframe.figure.clear()
        self.fxframe.figure.plot(self.xs, self.fx, "b-")
        self.fxframe.figure.set_xlabel("x")
        self.fxframe.figure.set_ylabel("f(x)")
        self.fxframe.figure.set_ylim(self.y1, self.y2)
        self.fxframe.figure.set_xlim(0, self.size-1)
        self.fxframe.canvas.show()
        
        self.fkframe.figure.clear()
        self.fkframe.figure.plot(self.ks[self.korder], self.fk.real[self.korder], "r-", label="Real")
        self.fkframe.figure.plot(self.ks[self.korder], self.fk.imag[self.korder], "g-", label="Imag.")
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
            self.singlek = self.xs_oversampled*0. + 1./self.size * self.fk[0]
        else:
            self.singlek = 1./self.size * (self.fk[self.sum_to] * np.exp(2.j*np.pi*self.k*self.xs_oversampled) + self.fk[self.size - self.sum_to] * np.exp(-2.j*np.pi*self.k*self.xs_oversampled))
    
    def show_ift(self):
        self.update()
        self.fxframe2.figure.clear()
        self.fxframe2.figure.plot(self.xs, self.fx2, "b-")
        self.fxframe2.figure.set_xlabel("x")
        self.fxframe2.figure.set_ylabel("f(x)")
        self.fxframe2.figure.set_ylim(self.y1, self.y2)
        self.fxframe2.canvas.show()
        
        self.fkframe2.figure.clear()
        self.fkframe2.figure.plot(self.ks[self.korder], self.fk2.real[self.korder], "r-", label="Real")
        self.fkframe2.figure.plot(self.ks[self.korder], self.fk2.imag[self.korder], "g-", label="Imag.")
        self.fkframe2.figure.set_xlabel("k")
        self.fkframe2.figure.set_ylabel("c(k)")
        self.fkframe2.figure.legend()
        self.fkframe2.canvas.show()
        
    def show_singlek(self):
        self.update()
        self.fxframe2.figure.clear()
        self.fxframe2.figure.plot(self.xs_oversampled, self.singlek.real, "b-")
        self.fxframe2.figure.set_xlabel("x")
        self.fxframe2.figure.set_ylabel("f(x)")
        if self.sum_to == 0:
            a = 2./self.size * np.absolute(self.fk[0])
            self.fxframe2.figure.set_title("f(x) = {0:.2}".format(a))
        else:
            a = 2./self.size * np.absolute(self.fk[self.sum_to])
            phi = np.angle(self.fk[self.sum_to], deg=False)
            self.fxframe2.figure.set_title("f(x) = {0:.2}cos(2pi{1:.2}x{2:+.2})".format(a, self.k, phi))
        self.fxframe2.figure.set_xlim(0, self.size-1)
        self.fxframe2.canvas.show()
        
        self.fkframe2.figure.clear()
        for i in range(self.sum_to):
            self.fk2[i] = 0.
        for i in range(self.size-self.sum_to+1, self.size):
            self.fk2[i] = 0.
        self.fkframe2.figure.plot(self.ks[self.korder], self.fk2.real[self.korder], "r-", label="Real")
        self.fkframe2.figure.plot(self.ks[self.korder], self.fk2.imag[self.korder], "g-", label="Imag.")
        self.fkframe2.figure.set_xlabel("k")
        self.fkframe2.figure.set_ylabel("c(k)")
        self.fkframe2.figure.legend()
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
    
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_pgf import FigureCanvasPgf as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
#from PyQt5.QtCore import QChar
import numpy as np
from scipy.optimize import curve_fit
from math import pi
import pylab
import matplotlib
from matplotlib import rc

#rc('text',usetex=True)
#rc('text.latex', preamble= r'\usepackage{color}')

def fit_func(x, c, a, tau, nu, phi):
    y=c+a*np.exp(-x/tau)*np.sin(2*pi*nu*x+phi)
    return y
class FitPanel(QWidget):
    def __init__(self, filepath, parent=None):
        super(FitPanel, self).__init__(parent)
        
        x=[]
        y=[]
        
        with open(filepath, 'r') as in_file:
            input=in_file.readlines()
            for line in input:
                if '#' in line or 'nan' in line:
                    continue
                x.append(float(line.split('\t')[1].strip('\n')))
                y.append(float(line.split('\t')[0]))
        self.x=np.asarray(x)/1000.
        self.y=np.asarray(y)
        self.popt=[1.,1.,1.,1.,1.]
        self.x_min=0
        self.x_max=self.x[len(self.x)-1]
        print('x_max value:'+str(self.x_max))
        self.plot=PlotCanvas(self.x, self.y, self.popt, self.x_min, self.x_max, self)

        self.initGUI()
        
        self.show()
        
    def initGUI(self):
        grid=QGridLayout(self)
        Fit_widget=QWidget(self)
        wgrid=QGridLayout(Fit_widget)
        vbox=QVBoxLayout(self)
        func_lbl=QLabel(u'Fit Function:\nC + A\u22C5e^(t/\u03C4)\u22C5sin(2\u03C0\u03BD\u22C5t + \u03C6)')
        par_lbl=QLabel('Set parameters boundaries:')
        fit_btn=QPushButton('Fit')
        t_lim_lbl=QLabel('Time interval in which to execute the fit: (default=all data)')
        fit_btn.clicked.connect(self.Fit)
        self.hboxes=[]
        self.WidgetsC=[]
        self.WidgetsA=[]
        self.WidgetsTau=[]
        self.WidgetsOmega=[]
        self.WidgetsPhi=[]
        self.WidgetsT=[]
        
        self.hboxes.append(self.create_par_box('C', self.WidgetsC)) 
        self.hboxes.append(self.create_par_box('A', self.WidgetsA))
        self.hboxes.append(self.create_par_box('\u03C4', self.WidgetsTau))
        self.hboxes.append(self.create_par_box('\u03BD', self.WidgetsOmega))
        self.hboxes.append(self.create_par_box('\u03C6', self.WidgetsPhi))
        self.hbox_t=self.create_par_box('t', self.WidgetsT)
        
        vbox.addStretch()
        vbox.addWidget(func_lbl)
        vbox.setSpacing(10)
        vbox.addWidget(par_lbl)
        vbox.setSpacing(10)
        for i, box in enumerate(self.hboxes):
            vbox.addLayout(box)
        vbox.setSpacing(20)
        vbox.addWidget(t_lim_lbl)
        vbox.addLayout(self.hbox_t)
        vbox.addWidget(fit_btn)
        vbox.addStretch()
        wgrid.addLayout(vbox, 0, 0)
        grid.addWidget(self.plot, 0, 0)
        grid.addWidget(Fit_widget, 0, 1, 1, 1)
        grid.setColumnMinimumWidth(0, 1300)
        self.setGeometry(450, 350, 1500, 800)
        self.setWindowTitle('Oscillator')
    def get_int(self, textwidg):
        num,ok = QInputDialog.getDouble(self,"insert number","enter a number")
		
        if ok:
            textwidg.setText(str(num))
    def create_par_box(self, name, Widgets):
        hbox=QHBoxLayout(self)
        #Widgets=[]
        Widgets.append(QLabel(name+' min:'))
        Widgets.append(QLineEdit())
        Widgets[1].setMaximumHeight(15)
        Widgets[1].setMaximumWidth(30)
        Widgets.append(QLabel(name+' max:'))
        Widgets.append(QLineEdit())
        Widgets[3].setMaximumHeight(15)
        Widgets[3].setMaximumWidth(30)
        hbox.addStretch()
        for i, W in enumerate(Widgets):
            hbox.addWidget(W)
            hbox.setSpacing(10)
        hbox.addStretch()

        return hbox
    def Fit(self):
        
        if self.WidgetsT[1].text()=='':
                self.x_min=0
        else:
            self.x_min=float(self.WidgetsT[1].text())
        if self.WidgetsT[3].text()=='':
            self.x_max=float(self.x[len(self.x)-1])
        else:
            self.x_max=float(self.WidgetsT[3].text())
        keep_going=True
        i=0
            
        while keep_going:
            if i<len(self.x):
                if self.x[i]<=self.x_min: 
                    self.i_min=i
                    #print(self.i_min)
                if self.x[i]<=self.x_max :
                    self.i_max=i
                else:
                    keep_going=False
                i+=1
            else:
                keep_going=False
        print(self.x[self.i_min:self.i_max])
        par_mins=[]
        par_maxs=[]
        try:
            par_mins.append(self.WidgetsC[1].text())
            par_maxs.append(self.WidgetsC[3].text())
            par_mins.append(self.WidgetsA[1].text())
            par_maxs.append(self.WidgetsA[3].text())
            par_mins.append(self.WidgetsTau[1].text())
            par_maxs.append(self.WidgetsTau[3].text())
            par_mins.append(self.WidgetsOmega[1].text())
            par_maxs.append(self.WidgetsOmega[3].text())
            par_mins.append(self.WidgetsPhi[1].text())
            par_maxs.append(self.WidgetsPhi[3].text())
            
            self.popt, self.pcov=curve_fit(fit_func, self.x[self.i_min:self.i_max], self.y[self.i_min:self.i_max], bounds=(par_mins, par_maxs))
            self.plot.axes.clear()
            self.plot.draw()
            self.plot.plot(self.x, self.y, self.popt, self.x_min, self.x_max)
            print('yeyeyeyeye')
        except:
            self.popt, self.pcov=curve_fit(fit_func, self.x[self.i_min:self.i_max], self.y[self.i_min:self.i_max])
            self.plot.axes.clear()
            self.plot.draw()
            self.plot.plot(self.x, self.y, self.popt, self.x_min, self.x_max)
        
class PlotCanvas(FigureCanvas):

    def __init__(self, x, y, popt,x_min, x_max, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.x=x
        self.y=y
        self.popt=popt
        self.x_min=x_min
        self.x_max=x_max
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot(self.x, self.y, self.popt, self.x_min, self.x_max)
        
 

    def plot(self, x, y, popt, x_min, x_max):
        ax = self.figure.add_subplot(111)
        ax.set_xlabel('time (s)')
        ax.set_ylabel('distance (cm)')
        x2=np.linspace(x_min, x_max, int(float(x_max-x_min)*100))
        y2=fit_func(x2, popt[0], popt[1], popt[2], popt[3], popt[4])
        ax.plot(x, y, label='Data')
        ax.plot(x2, y2, label='Fit')
        ax.legend()
        fit_string='Fitted values:\n'+'C: '+str(round(popt[0], 3))+'\nA: '+str(round(popt[1],3))+'\n\u03C4: '+str(round(popt[2],3))+'\n\u03BD: '+str(round(popt[3], 3))+'\n\u03C6: '+str(round(popt[4], 3))
        ax.text(0.95, 0.1, fit_string,
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        fontsize=15)
        #color='green', fontsize=15)
        
        ax.set_title('PyQt Matplotlib Example')
        self.draw()

    def clear(self):
        self.clear()

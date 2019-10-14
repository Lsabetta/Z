from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_pgf import FigureCanvasPgf as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
#from PyQt5.QtCore import QChar
import numpy as np
from scipy.optimize import curve_fit
from math import pi, isnan
import pylab
import matplotlib
from matplotlib import rc
from lmfit import Model
#rc('text',usetex=True)
#rc('text.latex', preamble= r'\usepackage{color}')

def fit_func(x, c, a, tau, nu, phi):
    y1=c
    y2=a*np.exp((-x)/float(tau))
    y3=np.sin(2*pi*nu*x+phi)
    return y1+y2*y3

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
        for i in range(len(x)):
            if isnan(x[i])or isnan(y[i]):
                print(x[i], y[i])
        self.results=[0 for i in range(len(x))]
        self.x_min=0
        self.x_max=self.x[len(self.x)-1]
        self.i_min=0
        self.i_max=len(x)
        print('x_max value:'+str(self.x_max))
        self.plot=PlotCanvas(self.x, self.y, self.results, self.i_min, self.i_max, self)
        self.fit_model=Model(fit_func)
        #self.params=self.fit_model.make_params(
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
                    
                if self.x[i]<=self.x_max :
                    self.i_max=i
                else:
                    keep_going=False
                i+=1
            else:
                keep_going=False
        
        par_mins=[]
        par_maxs=[]
        try:
            par_mins.append(float(self.WidgetsC[1].text()))
            par_maxs.append(float(self.WidgetsC[3].text()))
            par_mins.append(float(self.WidgetsA[1].text()))
            par_maxs.append(float(self.WidgetsA[3].text()))
            par_mins.append(float(self.WidgetsTau[1].text()))
            par_maxs.append(float(self.WidgetsTau[3].text()))
            par_mins.append(float(self.WidgetsOmega[1].text()))
            par_maxs.append(float(self.WidgetsOmega[3].text()))
            par_mins.append(float(self.WidgetsPhi[1].text()))
            par_maxs.append(float(self.WidgetsPhi[3].text()))
            self.fit_model.set_param_hint('c', value=(par_maxs[0]-par_mins[0])/2., min=par_mins[0], max=par_maxs[0])
            self.fit_model.set_param_hint('a', value=(par_maxs[1]-par_mins[1])/2., min=par_mins[1], max=par_maxs[1])
            self.fit_model.set_param_hint('tau', value=(par_maxs[2]-par_mins[2])/2., min=par_mins[2], max=par_maxs[2])
            self.fit_model.set_param_hint('nu', value=(par_maxs[3]-par_mins[3])/2., min=par_mins[3], max=par_maxs[3])
            self.fit_model.set_param_hint('phi', value=(par_maxs[4]-par_mins[4])/2., min=par_mins[4], max=par_maxs[4])
            
            self.params=self.fit_model.make_params()
            
            self.results=self.fit_model.fit(self.y[self.i_min:self.i_max], self.params, x=self.x[self.i_min:self.i_max])
            print("geppo")
        except:
            self.results=self.fit_model.fit(np.array(self.y[self.i_min:self.i_max]),a=1, c=1, nu=1, tau=1, phi=1, x=np.array(self.x[self.i_min:self.i_max]))
        self.best_fit=self.results.best_fit
        self.plot.axes.clear()
        self.plot.draw()
        self.plot.plot(self.x, self.y, self.best_fit, self.i_min, self.i_max, self.results)

        
class PlotCanvas(FigureCanvas):

    def __init__(self, x, y, results, i_min, i_max, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.x=x
        self.y=y
        self.results=results
        self.i_min=i_min
        self.i_max=i_max
        self.results_dic=0
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot(self.x, self.y, self.results, self.i_min, self.i_max, self.results_dic)
        
 

    def plot(self, x, y, results, i_min, i_max, results_dic):
        ax = self.figure.add_subplot(111)
        ax.set_xlabel('time (s)')
        ax.set_ylabel('distance (cm)')
        #x2=np.linspace(x_min, x_max, int(float(x_max-x_min)*100))
        x2=x[i_min:i_max]
        y2=results
        #y2=fit_func(x2, results[0], results[1], results[2], results[3], results[4])
        ax.plot(x, y, label='Data')
        ax.plot(x2, y2, label='Fit')
        ax.legend()
        if results_dic!=0:
            
            fit_string='Fitted values:\n'+'C: '+str(round(results_dic.best_values["c"], 3))+'\nA: '+str(round(results_dic.best_values["a"],3))+'\n\u03C4: '+str(round(results_dic.best_values["tau"],3))+'\n\u03BD: '+str(round(results_dic.best_values["nu"], 3))+'\n\u03C6: '+str(round(results_dic.best_values["phi"], 3))+'\nChi squared value:'+'\nchi: '+str(round(results_dic.chisqr, 3))
            ax.text(0.95, 0.1, fit_string,
                    verticalalignment='bottom', horizontalalignment='right',
                    transform=ax.transAxes,
                    fontsize=15)
            #color='green', fontsize=15)
        
        ax.set_title('PyQt Matplotlib Example')
        self.draw()

    def clear(self):
        self.clear()

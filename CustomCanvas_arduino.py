import numpy as np
import random as rd
import matplotlib
matplotlib.use("Qt4Agg")
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import time
import threading
from PyQt5.QtCore import Qt, QObject, pyqtSignal
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QWidget
class CustomFigCanvas(FigureCanvas, TimedAnimation):

    def __init__(self):

        self.addedData = []
        print(matplotlib.__version__)

        # The data
        self.xlim = 100
        self.n = np.linspace(0, self.xlim - 1, self.xlim)
        self.ticks_lbl=['0' for i in range(self.xlim)]
        self.ticks_pos=[int(np.linspace(0, 99, 5)[i]) for i in range(5)]
        self.ticks_lbl_reduced=[self.ticks_lbl[pos] for pos in self.ticks_pos]
        a = []
        b = []
        a.append(2.0)
        a.append(4.0)
        a.append(2.0)
        b.append(4.0)
        b.append(3.0)
        b.append(4.0)
        self.y = (self.n * 0.0) + 50

        # The window
        self.fig = Figure(figsize=(5,5), dpi=100)
        self.ax1 = self.fig.add_subplot(111)


        # self.ax1 settings
        self.ax1.set_xlabel('time')
        self.ax1.set_ylabel('raw data')
        self.line1 = Line2D([], [], color='blue')
        self.line1_tail = Line2D([], [], color='red', linewidth=2)
        self.line1_head = Line2D([], [], color='red', marker='o', markeredgecolor='r')
        self.ax1.add_line(self.line1)
        self.ax1.add_line(self.line1_tail)
        self.ax1.add_line(self.line1_head)
        self.ax1.set_xlim(0, self.xlim - 1)
        self.ax1.set_ylim(0, 250)
        self.ax1.set_xticklabels(self.ticks_lbl)


        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval = 50, blit = False)

    def new_frame_seq(self):
        return iter(range(self.n.size))

    def _init_draw(self):
        lines = [self.line1, self.line1_tail, self.line1_head]
        for l in lines:
            l.set_data([], [])

    def addData(self, value):
        self.addedData.append(value)

    def zoomIn(self, value):
        bottom = self.ax1.get_ylim()[0]
        top = self.ax1.get_ylim()[1]
        bottom += value
        top -= value
        self.ax1.set_ylim(bottom,top)
        self.draw()


    def _step(self, *args):
        # Extends the _step() method for the TimedAnimation class.
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            self.abc += 1
            print(str(self.abc))
            TimedAnimation._stop(self)
            pass

    def _draw_frame(self, framedata):
        margin = 2
        while(len(self.addedData) > 0):
            self.y = np.roll(self.y, -1)
            self.y[-1] = self.addedData[0][0]
            self.ticks_lbl =np.roll(self.ticks_lbl, -1)
            self.ticks_lbl=self.ticks_lbl.tolist()
            self.ticks_lbl[-1] = str(self.addedData[0][1])
            del(self.addedData[0])
        #print(self.ticks_lbl)
        self.ticks_lbl_reduced=[self.ticks_lbl[pos] for pos in self.ticks_pos]
        self.ax1.set_xticks(self.ticks_pos)
        self.ax1.set_xticklabels(self.ticks_lbl_reduced)
        self.line1.set_data(self.n[ 0 : self.n.size - margin ], self.y[ 0 : self.n.size - margin ])
        self.line1_tail.set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y[-10:-1 - margin], self.y[-1 - margin]))
        self.line1_head.set_data(self.n[-1 - margin], self.y[-1 - margin])
        self._drawn_artists = [self.line1, self.line1_tail, self.line1_head]

    def clear_plot(self):
        self.n = np.linspace(0, self.xlim - 1, self.xlim)
        self.y = (self.n * 0.0) + 50
        self.ticks_lbl=['0' for i in range(self.xlim)]
        #self.ticks_pos=[int(np.linspace(0, 99, 5)[i]) for i in range(5)]
        self.ticks_lbl_reduced=[self.ticks_lbl[pos] for pos in self.ticks_pos]
        self.ax1.set_xticks(self.ticks_pos)
        self.ax1.set_xticklabels(self.ticks_lbl_reduced)
        
class Communicate(QObject):
    data_signal = pyqtSignal(list)

''' End Class '''


def receiving(ser):
    last_received =''
    try:
        last_received=ser.readline().decode('utf8').strip('\r\n')
    except:
        last_received=''
    if ';' in last_received:
        try:
            return [float(last_received.split(';')[0]), float(last_received.split(';')[1])]
        except:
        
            return [last_received.split(';')[0], float(last_received.split(';')[1])] 
    else:
        return ['nan', 'nan']
            
def dataSendLoop(addData_callbackFunc, cond, go_ahead, acq_time, file_name):
    # Setup the signal-slot mechanism.
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'Generic CDC' in p.description  # may need tweaking to match new arduinos
    ]
    if not arduino_ports:
        raise IOError("No Arduino found")
    if len(arduino_ports) > 1:
        warnings.warn('Multiple Arduinos found - using the first')
           
    mySrc = Communicate()
    mySrc.data_signal.connect(addData_callbackFunc)
    with open(file_name, 'w') as out_file:
        
        with serial.Serial(arduino_ports[0], timeout=acq_time[0]) as ard:
            a=0
            i=0
            start=0
            now=0
            out=[]
            out_file.write('#distance(cm)\t time(ms) \n')
            print(file_name)
            while (now)<acq_time[0]:
                if go_ahead[0]:

                    out.append(receiving(ard))
                    if out[i][0]!='nan' and i>50:
                        if i==51:
                            start=out[i][1]
                        now=out[i][1]-start
                        out[i][1]=now
                        out[i][0]=out[i][0]*0.034/2
                        mySrc.data_signal.emit(out[i])   # <- Here you emit a signal!
                        out_file.write(str(out[i][0])+'\t'+str(out[i][1])+'\n')
                    i+=1
                    
                else:
                    with cond:
                        cond.wait()
    '''
    if cb_state==1:
        #Data_Window= Pop_Data()
        Data_Window.open_file(file_name)
        Data_Window.show()
     #   with open(file_name, 'r') as data_file;
    '''

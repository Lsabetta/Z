import sys, os
#from PyQt5.QtWidgets import (QCheckBox, QFileDialog, QMessageBox, QErrorMessage, QFileDialog, QInputDialog, QLineEdit, QFrame, QComboBox, QTextEdit, QGridLayout, QWidget, QMainWindow, QAction, qApp, QApplication, QMenu, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLCDNumber, QSlider)
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QObject, pyqtSignal 
from CustomCanvas_arduino import *
from fit_try import *
import time
import StoppableThread
class Start_Oscillatore(QMainWindow):
    def __init__(self, parent=None):
        super(Start_Oscillatore, self).__init__(parent)
        self.CWidget=QWidget(parent=self)
        self.setCentralWidget(self.CWidget)

        start_grid=QGridLayout(self.CWidget)
        
        vbox_file=QVBoxLayout(self.CWidget)
        self.CWidget.file_btn=QPushButton('File pattern:')
        self.CWidget.file_lineedit = QLineEdit(self) 
        vbox_file.addWidget(self.CWidget.file_btn)
        vbox_file.addWidget(self.CWidget.file_lineedit)
        self.file_name=''
        self.CWidget.file_btn.clicked.connect(self.get_file)
        self.CWidget.file_lineedit.textChanged.connect(self.set_file_name)
        vbox_file.setSpacing(0.1)
        
        vbox_acq_time=QVBoxLayout(self.CWidget)
        self.CWidget.acq_time_btn=QPushButton('Acquisition time(s):')
        self.CWidget.acq_time_lineedit = QLineEdit(self)
        vbox_acq_time.addWidget(self.CWidget.acq_time_btn)
        vbox_acq_time.addWidget(self.CWidget.acq_time_lineedit)
        self.CWidget.acq_time_btn.clicked.connect(self.get_int)
        self.CWidget.acq_time_lineedit.textChanged.connect(self.set_acq_time)
        vbox_acq_time.setSpacing(0.1)

        hbox_buttons=QHBoxLayout(self.CWidget)
        self.CWidget.Begin_btn=QPushButton('Begin')
        self.CWidget.Begin_btn.clicked.connect(self.Begin)
        hbox_buttons.addWidget(self.CWidget.Begin_btn)
        self.CWidget.Clear_btn=QPushButton('Clear')
        self.CWidget.Clear_btn.clicked.connect(self.Clear)
        hbox_buttons.addWidget(self.CWidget.Clear_btn)
        self.CWidget.Display_Data_btn=QPushButton('Display Data')
        self.CWidget.Display_Data_btn.clicked.connect(self.Display_Data)
        hbox_buttons.addWidget(self.CWidget.Display_Data_btn)
        hbox_buttons.setSpacing(0.3)
        
        self.CWidget.Fit_btn=QPushButton('Plot&Fit')
        self.CWidget.Fit_btn.clicked.connect(self.Fit)
        
        self.CWidget.myplot=CustomFigCanvas()
        self.acq_time=[10000]
        self.cond=threading.Condition()
        self.go_ahead=[1]
        self.go_ahead_copy=self.go_ahead
        
        start_grid.addWidget(self.CWidget.myplot, 0, 0, 2, 2)
        
        start_grid.addLayout(vbox_acq_time, 2,1)
        start_grid.addLayout(vbox_file, 2,0)
        start_grid.addLayout(hbox_buttons, 3, 1)
        start_grid.addWidget(self.CWidget.Fit_btn, 3, 0)
        
        '''
        StartAct = QAction(QIcon('../icons/play.png'), '&Start', self)
        StartAct.setShortcut('Ctrl+S')
        StartAct.setStatusTip('Play')
        StartAct.triggered.connect(self.Start)                                                                                                                  


        PauseAct= QAction(QIcon('../icons/pause.png'), '&Pause', self)
        PauseAct.setStatusTip('Pause')
        PauseAct.setShortcut('Ctrl+P')
        PauseAct.triggered.connect(self.Pause)
        '''
        StopAct=QAction(QIcon('icons/Stop_icon.png'), '&Stop', self)
        StopAct.setStatusTip('Stop')
        StopAct.setShortcut('Ctrl+S')
        StopAct.triggered.connect(self.Stop)
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.setMovable(False)
        #self.toolbar.addAction(StartAct)
        #self.toolbar.addAction(PauseAct)
        self.toolbar.addAction(StopAct)

        self.setGeometry(400, 350, 1000, 800)
        self.setWindowTitle('Oscillator')
        
    def addData_callbackFunc(self, value):
        #print(value)
        self.CWidget.myplot.addData(value)

    def Begin(self):
        
        if self.CWidget.acq_time_lineedit.text()=="" or self.CWidget.file_lineedit.text()=="":
            rtrn=QMessageBox.warning(self, "Warning", "Required argument missing")
        else:
            self.acq_time[0]=int(float(self.CWidget.acq_time_lineedit.text())*1000)
            self.myDataLoop = threading.Thread(name = 'myDataLoop', target = dataSendLoop, daemon = True, args = (self.addData_callbackFunc,
                                                                                                                  self.cond, self.go_ahead_copy, self.acq_time, self.file_name))

            if self.myDataLoop.is_alive()==False:
                print("loop is: ", self.myDataLoop.is_alive())
                self.myDataLoop.start()
                time.sleep(0.1)
                with self.cond:
                    self.cond.notify()
            else:
                print("loop is: ", self.myDataLoop.is_alive())
                print("amd now it is: ", self.myDataLoop.is_alive())

    def Clear(self):
        self.CWidget.acq_time_lineedit.setText('')
        self.CWidget.file_lineedit.setText('')
        self.CWidget.myplot.clear_plot()
        
    def Start(self):
        if self.myDataLoop.is_alive()==False:
            time.sleep(0.1)
            print("loop is: ", self.myDataLoop.is_alive())
        else:
            
            if self.go_ahead[0]==0:
                with self.cond:
                    self.go_ahead[0]=1
                    self.cond.notify()
                    time.sleep(0.1)

    def Pause(self):
        self.go_ahead[0]=0

    def Stop(self):
        self.acq_time[0]=0

    def Fit(self):
        self.fit_panel=FitPanel(self.file_name)
    def get_int(self):
        num,ok = QInputDialog.getInt(self,"Acquisition time(s)","enter a number")
		
        if ok:
            self.CWidget.acq_time_lineedit.setText(str(num))
            

    def get_file(self):
       
        name= QFileDialog.getSaveFileName(self, "Save File name", "", " All Files(*);; Text Files (*.txt)", options=QFileDialog.DontConfirmOverwrite)
        self.CWidget.file_lineedit.setText(str(name))
        
    def set_acq_time(self):
        try:
            self.acq_time[0]=int(float(self.CWidget.acq_time_lineedit.text())*1000)
            print(self.acq_time)
        except:
            time.sleep(0.1)
    def set_file_name(self):
        try:
            self.file_name=self.CWidget.file_lineedit.text()
            if "(" in self.file_name:
                self.file_name= self.file_name.split("(")[1].split("'")[1]

        except:
            time.sleep(0.1)

    def Display_Data(self):
        try:
            self.Data_Window= Pop_Data()
            self.Data_Window.open_file(self.file_name)
            self.Data_Window.show()
        except:
            time.sleep(0.1)
        
class Pop_Data(QWidget):
    def __init__(self, parent=None):
        super(Pop_Data, self).__init__(parent)
        grid=QGridLayout(self)
        self.setGeometry(500, 400, 1000, 800)
        self.Text=QTextEdit(self)
        #self.Text.setGeometry(300, 300, 1000, 800)
        grid.addWidget(self.Text, 0, 0)
        
    def open_file(self, file_name):
        with open(file_name, 'r') as f:
            self.setWindowTitle(file_name)
            self.Text.setText(f.read())

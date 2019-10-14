import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from Start_Oscillatore_arduino import *

class Z(QMainWindow): #Main class, is the skeleton of the first window that pop up when Z is called
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):#In this init the skeleton of the window is made, and a Content class is created (defined later on in the code)                
        self.Content_widget=Content(parent=self)#Class in which all the usefull buttons are actually placed
        self.setCentralWidget(self.Content_widget)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        ####
        #couple of action that could be usefull. More can be added
        exitAct = QAction(QIcon('icons/Actions-application-exit-icon.png'), '&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        
        viewStatAct= QAction('view statusbar', self, checkable=True)
        viewStatAct.setStatusTip('View statusbar')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.toggleMenu)
        #
        
        ####
        #Creating a menuBar with voices connect to the actions defined 
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        viewMenu= menubar.addMenu('&View')
        viewMenu.addAction(viewStatAct)
        #
        
        ####
        #Creating ToolBar, where actions can be added as buttons with icons
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.setMovable(False)
        self.toolbar.addAction(exitAct)
        #
        
        self.setGeometry(300, 300, 1000, 800)
        self.setWindowTitle('Z')    
        self.show()
    ####
    #function connected to ViewStatAct
    def toggleMenu(self, stato):
        if stato:
            self.statusbar.show()
        else:
            self.statusbar.hide()
    #
    
    ####
    #right-click menu
    def contextMenuEvent(self, event):
        cmenu = QMenu(self)    
        newAct = cmenu.addAction("New")
        opnAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
           
        if action == quitAct:
            qApp.quit()
    #
class Content(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        ####
        # create and set layout to place widgets
        grid_layout = QGridLayout(self)
        grid_layout.setSpacing(1)
        self.setLayout(grid_layout)
        #
        ####
        #Image logo
        self.logo = QLabel(self)
        self.pixmap = QPixmap('icons/Z_logo.png')
        self.logo.setPixmap(self.pixmap)
        #
        
        #####
        #Experience selection widget
        self.set_option_lbl=QLabel(self)
        self.set_option_lbl.setText('Select the experience:')
        
        self.combo=QComboBox(self)
        options=['Oscillator', 'prova1', 'prova2', 'prova3', 'prova4']
        for option in options:
            self.combo.addItem(option)
            
        hbox=QHBoxLayout(self)
        hbox.addWidget(self.set_option_lbl)
        hbox.addWidget(self.combo)
        #
        
        ####
        #buttons
        self.start_button = QPushButton('Start')
        self.clear_button = QPushButton('Clear')
        self.cancel_button = QPushButton('Cancel')
        self.start_button.clicked.connect(self.on_start_button_clicked)
        #
        
        ####
        # add widgets to layout. Params are:
        # (widget, fromRow, fromColumn, rowSpan=1, columnSpan=1)
        
        grid_layout.addWidget(self.logo, 0, 0, 3, 3)
        grid_layout.addLayout(hbox, 3, 0)
        grid_layout.addWidget(self.start_button, 4, 0)
        grid_layout.addWidget(self.clear_button, 4, 1)
        grid_layout.addWidget(self.cancel_button, 4, 2)
        #
    ####
    #Function connected to the start button
    def on_start_button_clicked(self):
        if self.combo.currentText()=='Oscillator':
            self.start_oscillatore=Start_Oscillatore(self)
            self.start_oscillatore.show()
        else:
            #add other options when other experiences will be ready
            print('')
    #
        

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Z()
    sys.exit(app.exec_())





































    

import pyaudio
import numpy as np
import pyqtgraph as pg
import PySide 
#import Devices
#import Screen
#import Equipment as myEq
import Instruments.oscilloscope as myScope
import Instruments.spectrumAnalyzer as myAnalyzer


#class SpectrumAnalyzer(pg.GraphicsWindow):
class MainWindow(PySide.QtGui.QWidget):
    """docstring for ClassName"""
    def __init__ (self, parent = None):  
        super(MainWindow, self).__init__(parent)
        self.resize(700, 700)      
        self.setWindowTitle("Measurment Equipment")  
        self.UIsetup()
        self.ON_OFF = False   # False means OFF

    def UIsetup(self):
        ''' Create tabs'''
        self.tabs = PySide.QtGui.QTabWidget()
        #self.tab2 = PySide.QtGui.QTabWidget()   # Spectrum Analyzer
        # self.tabs.addTab(myEq.spectrumAnalyzer(),"Spectrum Analyzer")
        # self.tabs.addTab(myEq.oscilloscope(),"Oscilloscope")
        # self.tabs.addTab(PySide.QtGui.QWidget(),"Functions Generator")
        self.tabs.addTab(myAnalyzer.spectrumAnalyzer(),"Spectrum Analyzer")
        self.tabs.addTab(myScope.oscilloscope(),"Oscilloscope")
        self.tabs.addTab(PySide.QtGui.QWidget(),"Functions Generator")
		
        self.tabs.resize(600, 600)

        ''' Layouts '''        
        self.mainLayout = PySide.QtGui.QVBoxLayout()
        self.mainLayout.addWidget(self.tabs)
        self.setLayout(self.mainLayout)

if __name__ == '__main__':
    app = PySide.QtGui.QApplication([])   
    s = MainWindow()
    s.show()       
    app.exec_()
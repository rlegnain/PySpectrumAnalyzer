import pyaudio
import numpy as np
import pyqtgraph as pg
import PySide 
import Devices
import Screen
import Equipment as myEq

CHUNK = 1024    #  CHUNK is power of 2
samlingRate = 44100 # sampling/second
CHANNELS = 1
FORMAT = pyaudio.paInt16

OneSideFFT_points = CHUNK/2 + 1      #Calculate the of one-side FFF points.
window = np.ones(CHUNK)

#class SpectrumAnalyzer(pg.GraphicsWindow):
class MainWindow(PySide.QtGui.QWidget):
    """docstring for ClassName"""

    def __init__ (self, parent = None):  
        super(MainWindow, self).__init__(parent)
        self.resize(700, 700)      
        self.setWindowTitle("Measurment Equipment")  
        self.UIsetup()
        self.device =  Devices.sundCardDevice(FORMAT, CHANNELS, samlingRate, CHUNK)
        self.ON_OFF = False   # False means OFF

    def UIsetup(self):
        ''' Create tabs'''
        self.tabs = PySide.QtGui.QTabWidget()
        self.tab2 = PySide.QtGui.QTabWidget()   # Spectrum Analyzer
        self.tabs.addTab(myEq.spectrumAnalyzer(),"Spectrum Analyzer")
        self.tabs.addTab(myEq.oscilloscope(),"Oscilloscope")
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
import pyaudio
import numpy as np
import pyqtgraph as pg
import  PySide 

CHUNK = 1024    #
samlingRate = 44100 # sampling/second
CHANNELS = 1
FORMAT = pyaudio.paInt16
freqRange = np.arange(-CHUNK/2 , CHUNK/2)/float(CHUNK)*float(samlingRate)


#class SpectrumAnalyzer(pg.GraphicsWindow):
class SpectrumAnalyzer(PySide.QtGui.QWidget):
    """docstring for ClassName"""

    def __init__ (self, parent = None):  
        super(SpectrumAnalyzer, self).__init__(parent)
        self.resize(700, 700)      
        self.setWindowTitle("Spectrum Analyzer")  
        self.UIsetup()
        self.ON_OFF = False   # False means OFF

    def UIsetup(self):

        self.ScreenTIME = pg.PlotWidget(background=(0, 0, 0))  # define plot windows
        self.ScreenTIME.setRange(yRange=[-4000,4000])
        self.ScreenTIME.showGrid(x = True, y = True, alpha = 0.3) 
        self.timePlot  = self.ScreenTIME.plot(pen='y', )

        self.ScreenFFT = pg.PlotWidget( background=(0, 0, 0))  # define plot windows
        self.ScreenFFT.setRange(yRange=[5,300000])
        self.ScreenFFT.showGrid(x = True, y = True, alpha = 0.3) 
        self.fftPlot  = self.ScreenFFT.plot(pen='y', )


        self.BtnPower = PySide.QtGui.QPushButton("OFF")
        #self.BtnPower.setStyleSheet('QPushButton {color: red}')

        self.Grid = PySide.QtGui.QGridLayout() 
        self.Grid.setSpacing(10)
        self.Grid.addWidget(self.ScreenTIME, 0,0,16,12)
        self.Grid.addWidget(self.ScreenFFT, 17,0,16,12)

        self.Grid.addWidget(self.BtnPower, 0,13)
        self.setLayout(self.Grid)
        self.show()
        

        #QtCore.QObject.connect(button, QtCore.SIGNAL ('clicked()'), someFunc)
        self.BtnPower.clicked.connect(self.BtnPower_clicked)


    def BtnPower_clicked(self):
        if self.ON_OFF :
            self.TurnOFF()
            self.ON_OFF = False
            self.BtnPower.setText("OFF")
            #self.BtnPower.setStyleSheet('QPushButton {color: red}')

        else:
            self.TurnON()
            self.ON_OFF = True
            self.BtnPower.setText("ON")
            #self.BtnPower.setStyleSheet('QPushButton {color: green}')


    def TurnON(self):    
        self.openPort()
        self.t = PySide.QtCore.QTimer()
        self.t.timeout.connect(self.update)
        self.t.start(50) #QTimer takes ms

    def TurnOFF(self):
        self.t.stop()
    
    def openPort(self):   
        self.p = pyaudio.PyAudio()
        self.Stream = self.p.open(format = FORMAT, channels = CHANNELS, rate = samlingRate, input = True, frames_per_buffer = CHUNK)
  
    def readSignal(self):
        signal = self.Stream.read(CHUNK)
        data = np.fromstring(signal, dtype=np.int16)
        return data
    
    def closePort(self):
        self.Stream.stop_stream()
        self.Stream.close()
        self.p.terminate()

    def update(self):
        timeSignal = self.readSignal()
        freqSignal = np.fft.fftshift(np.abs(np.fft.fft(timeSignal)))  
        freqSignal_dB = 10*np.log10(freqSignal)
        self.timePlot.setData(freqRange, timeSignal)
        self.fftPlot.setData(freqRange, freqSignal)


if __name__ == '__main__':
    app = PySide.QtGui.QApplication([])   
    s = SpectrumAnalyzer()

    
        
    app.exec_()
    

import pyaudio
import numpy as np
import pyqtgraph as pg
import PySide 

CHUNK = 1024    #
samlingRate = 44100 # sampling/second
CHANNELS = 1
FORMAT = pyaudio.paInt16
#freqRange = np.arange(-CHUNK/2 , CHUNK/2)/float(CHUNK)*float(samlingRate)  # two-side fourier transform
freqRange = np.arange(0 , CHUNK)/float(CHUNK)*float(samlingRate)
window = np.ones(CHUNK)

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
        ''' Creeate screen to plot TIME domain'''
        self.ScreenTIME = pg.PlotWidget(background=(0, 0, 0))  # define plot windows
        self.ScreenTIME.setRange(yRange=[-4000,4000])
        self.ScreenTIME.showGrid(x = True, y = True, alpha = 0.3) 
        self.timePlot  = self.ScreenTIME.plot(pen='y', )
        ''' Create screen to plot Frequency domain  '''
        self.ScreenFFT = pg.PlotWidget( background=(0, 0, 0))  # define plot windows
        self.ScreenFFT.setRange(yRange=[5,300000])
        self.ScreenFFT.showGrid(x = True, y = True, alpha = 0.3) 
        self.fftPlot  = self.ScreenFFT.plot(pen='y', )

        ''' Create power ON/OFF button '''
        self.BtnPower = PySide.QtGui.QPushButton("OFF")
        #self.BtnPower.setStyleSheet('QPushButton {color: red}')
        
        ''' Create List box of Windows functions Menu'''
        self.comBoxWinFunction = PySide.QtGui.QComboBox()
        self.comBoxWinFunction.addItem("Rectangular")
        self.comBoxWinFunction.addItem("Hamming ")

        ''' Layouts '''
        self.Grid = PySide.QtGui.QGridLayout() 
        self.Grid.setSpacing(10)
        self.Grid.addWidget(self.ScreenTIME, 0,0,16,12)
        self.Grid.addWidget(self.ScreenFFT, 17,0,16,12)

        self.Grid.addWidget(self.BtnPower, 0,13)
        self.Grid.addWidget(self.comBoxWinFunction, 1,13)



        self.setLayout(self.Grid)
        self.show()
        

        #QtCore.QObject.connect(button, QtCore.SIGNAL ('clicked()'), someFunc)
        self.BtnPower.clicked.connect(self.BtnPower_clicked)
        self.comBoxWinFunction.currentIndexChanged[int].connect(self.SelectWindowsFun)


    def SelectWindowsFun(self, index):
        global window
        if index == 0:
            window = np.ones(CHUNK)
        elif index== 1:
            window = np.hamming(CHUNK)


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
        self.SignalProcessing()

    def SignalProcessing(self):        
        global window
        timeSignal = self.readSignal()*window
        self.timePlot.setData(freqRange, timeSignal)
        #freqSignal = np.fft.fftshift(np.abs(np.fft.fft(timeSignal)))  # plot two side fourier transform
        freqSignal = np.abs(np.fft.fft(timeSignal))  # plot one-side fourier transform
        freqSignal_dB = 10*np.log10(freqSignal)
        self.fftPlot.setData(freqRange[0:CHUNK/2-1], freqSignal[0:CHUNK/2-1])


if __name__ == '__main__':
    app = PySide.QtGui.QApplication([])   
    s = SpectrumAnalyzer()

    
        
    app.exec_()
    

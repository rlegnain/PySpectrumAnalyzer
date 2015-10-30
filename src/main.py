import pyaudio
import numpy as np
import pyqtgraph as pg
import PySide 
import Devices


CHUNK = 1024    #  CHUNK is power of 2
samlingRate = 44100 # sampling/second
CHANNELS = 1
FORMAT = pyaudio.paInt16

OneSideFFT_points = CHUNK/2 + 1      #Calculate the of one-side FFF points.
window = np.ones(CHUNK)

#class SpectrumAnalyzer(pg.GraphicsWindow):
class SpectrumAnalyzer(PySide.QtGui.QWidget):
    """docstring for ClassName"""

    def __init__ (self, parent = None):  
        super(SpectrumAnalyzer, self).__init__(parent)
        self.resize(700, 700)      
        self.setWindowTitle("Spectrum Analyzer")  
        self.UIsetup()
        self.device =  Devices.sundCardDevice(FORMAT, CHANNELS, samlingRate, CHUNK)

        self.ON_OFF = False   # False means OFF

    def UIsetup(self):
        ''' Creeate screen to plot TIME domain'''
        self.ScreenTIME = pg.PlotWidget(background=(0, 0, 0))  # define plot windows
        self.ScreenTIME.setRange(yRange=[-2000,2000])
        self.ScreenTIME.showGrid(x = True, y = True, alpha = 0.3) 
        self.timePlot  = self.ScreenTIME.plot(pen='y', )
        self.ScreenTIME.setLabels(left=('Amplitue')) 
        self.ScreenTIME.setLabels(bottom=('Time (ms)')) 


        ''' Create screen to plot Frequency domain  '''
        self.ScreenFFT = pg.PlotWidget( background=(0, 0, 0))  # define plot windows
        self.ScreenFFT.setRange(yRange=[0,1000])
        self.ScreenFFT.showGrid(x = True, y = True, alpha = 0.3) 
        self.fftPlot  = self.ScreenFFT.plot(pen='y', )
        self.ScreenFFT.setLabels(left=('Magnitude')) 
        self.ScreenFFT.setLabels(bottom=('Frequency (Hz)')) 

        ''' Create power ON/OFF button '''
        self.BtnPower = PySide.QtGui.QPushButton("OFF")
        #self.BtnPower.setStyleSheet('QPushButton {color: red}')        
        ''' Create List box of Windows functions Menu'''
        self.comBoxWinFunction = PySide.QtGui.QComboBox()
        self.comBoxWinFunction.addItem("Rectangular")
        self.comBoxWinFunction.addItem("Hamming ")
        self.comBoxWinFunction.addItem("Hanning ")
        self.comBoxWinFunction.addItem("Bartlett ")
        self.comBoxWinFunction.addItem("Blackman ")

        ''' Create list box of channes menu'''
        self.comBoxChannelList = PySide.QtGui.QComboBox()
        self.comBoxChannelList.addItem("Channel 1")
        self.comBoxChannelList.addItem("Channel 2")
        self.comBoxChannelList.addItem("Both channels")


        ''' Layouts '''
        ''' Screen layout '''
        self.screenLyout = PySide.QtGui.QVBoxLayout()
        self.screenLyout.addWidget(self.ScreenTIME,)
        self.screenLyout.addWidget(self.ScreenFFT)


        ''' Parameter Layout'''
        self.ParameterLyout = PySide.QtGui.QVBoxLayout()
        self.ParameterLyout.addWidget(self.BtnPower)
        self.ParameterLyout.addWidget(self.comBoxWinFunction)
        self.ParameterLyout.addWidget(self.comBoxChannelList)
        
        


        ''' All Layout'''
        self.Grid = PySide.QtGui.QGridLayout() 
        self.Grid.setSpacing(10)
        self.Grid.addLayout(self.screenLyout, 0,0,16,24)
        self.Grid.addLayout(self.ParameterLyout, 0,25)

        self.setLayout(self.Grid)
        self.show()
        

        #QtCore.QObject.connect(button, QtCore.SIGNAL ('clicked()'), someFunc)
        self.BtnPower.clicked.connect(self.BtnPower_clicked)
        self.comBoxWinFunction.currentIndexChanged[int].connect(self.SelectWindowsFun)
        self.comBoxChannelList.currentIndexChanged[int].connect(self.selectChannel)
   
    def selectChannel(self, index):
        global window
        if   index == 0:
            CHANNELS = 1
        elif index == 2:
            CHANNELS = 1
        elif index == 3:
            CHANNELS = 1

    def SelectWindowsFun(self, index):
        global window
        if   index == 0:
            window = np.ones(CHUNK)
        elif index == 1:
            window = np.hamming(CHUNK)
        elif index == 2:
            window = np.hanning(CHUNK)
        elif index == 3:
            window = np.bartlett(CHUNK)
        elif index == 4:
             window = np.blackman(CHUNK)



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
        self.device.openPort()
        self.t = PySide.QtCore.QTimer()
        self.t.timeout.connect(self.update)
        self.t.start(50) # QTimer takes ms

    def TurnOFF(self):
        self.t.stop()
    

    def update(self):        
        self.plotOnScreen()

    def calculateFFT(self):
        global window
        timeSignal = self.device.readSignal()*window
        TwoSideFFT = np.fft.fft(timeSignal)/ (CHUNK)   # Two-side FFT.   We devided by CHUNK (please revise FFT)
        OneSideFFT = 2 * TwoSideFFT[0 : OneSideFFT_points]  # we multiply by 2, because we remove the second FFT side (read FFT)
        MagnitudeFFT = np.abs(OneSideFFT)
        #freqSignal_dB = 10*np.log10(freqSignal)
        timeRange = np.arange(0 , CHUNK) / float(samlingRate)
        freqRange = np.arange(0 , OneSideFFT_points) * (float(samlingRate)/ float(CHUNK))

        return timeSignal, MagnitudeFFT, timeRange, freqRange

    def plotOnScreen(self):
        timeSignal, MagnitudeFFT, timeRange, freqRange  = self.calculateFFT()
        self.timePlot.setData(timeRange, timeSignal)
        self.fftPlot.setData(freqRange, MagnitudeFFT)


if __name__ == '__main__':
    app = PySide.QtGui.QApplication([])   
    s = SpectrumAnalyzer()

    
        
    app.exec_()
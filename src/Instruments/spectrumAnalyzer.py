import pyaudio
import numpy as np
import pyqtgraph as pg
from PySide import QtCore, QtGui
#import Devices
import Interface.soundCard as Devices
import Screen

CHUNK = 1024    #  CHUNK is power of 2
samlingRate = 44100 # sampling/second
CHANNELS = 2
FORMAT = pyaudio.paInt32

OneSideFFT_points = CHUNK/2 + 1      #Calculate the of one-side FFF points.
window = np.ones(CHUNK)

class spectrumAnalyzer(QtGui.QWidget):
    def __init__(self, parent=None):
        super(spectrumAnalyzer, self).__init__(parent)

        self.device =  Devices.sundCardDevice(FORMAT, CHANNELS, samlingRate, CHUNK)
        self.ON_OFF = False   # False means OFF

        ''' Create Widget for screen'''
        self.ScreenFFT =  Screen.Display("Frequency (Hz)", "Magnitude",  [0,8000], [0,10000000])
        self.fftPlot = self.ScreenFFT.plot(pen='y', )
        
        ''' Create list box of Frequency range'''
        self.FreqRangeGroup = QtGui.QGroupBox("Frequency Rang (Hz)")
        self.FreRangeLayout = QtGui.QGridLayout()
        self.SpinBoxStartFreq = QtGui.QSpinBox()
        self.SpinBoxStopFreq  = QtGui.QSpinBox()
        self.LabelStartFreq = QtGui.QLabel("Start")
        self.LabelStopFreq  = QtGui.QLabel("Stop")
        self.SpinBoxStartFreq.setMinimum(0)
        self.SpinBoxStartFreq.setMaximum(1000000)
        self.SpinBoxStopFreq.setMinimum(0)
        self.SpinBoxStopFreq.setMaximum(1000000000)
        self.SpinBoxStartFreq.setValue(0)
        self.SpinBoxStopFreq.setValue(1000)
        self.FreRangeLayout.addWidget(self.LabelStartFreq,0,0)
        self.FreRangeLayout.addWidget(self.LabelStopFreq,1,0)
        self.FreRangeLayout.addWidget(self.SpinBoxStartFreq,0,1)
        self.FreRangeLayout.addWidget(self.SpinBoxStopFreq,1,1)
        self.FreqRangeGroup.setLayout(self.FreRangeLayout)
        self.SpinBoxStartFreq.valueChanged[int].connect(self.StartFreqChanged)
        self.SpinBoxStopFreq.valueChanged[int].connect(self.StopFreqChanged)

        ''' Create List box of Windows functions Menu'''
        self.comBoxWinFunction = QtGui.QComboBox()
        self.comBoxWinFunction.addItem("Rectangular")
        self.comBoxWinFunction.addItem("Hamming ")
        self.comBoxWinFunction.addItem("Hanning ")
        self.comBoxWinFunction.addItem("Bartlett ")
        self.comBoxWinFunction.addItem("Blackman ")

        ''' Create power ON/OFF button '''
        self.BtnPower = QtGui.QPushButton("OFF")
        #self.BtnPower.setStyleSheet('QPushButton {color: red}')  

        ''' Layouts '''
        self.mainLayout = QtGui.QVBoxLayout()       # Main  Layout (Horizontal)

        self.ParameterLayout =  QtGui.QGridLayout() # parameter Laygout Grid
        self.ParameterLayout.setSpacing(10)
        self.ParameterLayout.addWidget(self.FreqRangeGroup, 0,0)
        self.ParameterLayout.addWidget(self.comBoxWinFunction, 0,1)
        self.ParameterLayout.addWidget(self.BtnPower, 0,2)

        self.mainLayout.addWidget(self.ScreenFFT)
        self.mainLayout.addLayout(self.ParameterLayout)

        self.setLayout(self.mainLayout )


        #QtCore.QObject.connect(button, QtCore.SIGNAL ('clicked()'), someFunc)
        self.BtnPower.clicked.connect(self.BtnPower_clicked)
        self.comBoxWinFunction.currentIndexChanged[int].connect(self.SelectWindowsFun)

    def StartFreqChanged(self, value_as_int):
		xLimit = [value_as_int , self.SpinBoxStopFreq.value()]
		self.ScreenFFT.setRange(xRange=xLimit)

    def StopFreqChanged(self, value_as_int):
		xLimit = [self.SpinBoxStartFreq.value() , value_as_int]
		self.ScreenFFT.setRange(xRange=xLimit)

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
        self.t = QtCore.QTimer()
        self.t.timeout.connect(self.update)
        self.t.start(50) # QTimer takes ms

    def TurnOFF(self):
        self.t.stop()
    

    def update(self):        
        self.plotOnScreen()

    def calculateFFT(self):
        global window
        CH1, CH2 = self.device.readSignal()
        timeSignalCH1 = CH1*window
        timeSignalCH2 = CH2*window
        TwoSideFFT = np.fft.fft(timeSignalCH1)/ (CHUNK)   # Two-side FFT.   We devided by CHUNK (please revise FFT)
        OneSideFFT = 2 * TwoSideFFT[0 : OneSideFFT_points]  # we multiply by 2, because we remove the second FFT side (read FFT)
        MagnitudeFFT = np.abs(OneSideFFT)
        #freqSignal_dB = 10*np.log10(freqSignal)
        timeRange = np.arange(0 , CHUNK) / float(samlingRate)
        freqRange = np.arange(0 , OneSideFFT_points) * (float(samlingRate)/ float(CHUNK))

        return MagnitudeFFT, freqRange

    def plotOnScreen(self):
        MagnitudeFFT, freqRange  = self.calculateFFT()
        self.fftPlot.setData(freqRange, MagnitudeFFT)


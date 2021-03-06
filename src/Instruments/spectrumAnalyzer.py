import pyaudio
import numpy as np
import pyqtgraph as pg
from PySide import QtCore, QtGui
#import Devices
import Interface.soundCard as Devices
import Instruments.Screen as Screen

#CHUNK = 2048    #  CHUNK is power of 2
#samlingRate = 88200 # sampling/second
#CHANNELS = 2
#FORMAT = pyaudio.paInt16

#OneSideFFT_points = CHUNK/2 + 1      #Calculate the of one-side FFF points.
#window = np.ones(CHUNK)

class spectrumAnalyzer(QtGui.QWidget):
    def __init__(self, parent=None):
        super(spectrumAnalyzer, self).__init__(parent)
		
		
        self.device =  Devices.sundCardDevice()
        self.CHUNK = self.device.CHUNK    #  CHUNK is power of 2
        self.samlingRate = self.device.samlingRate # sampling/second
        self.CHANNELS = self.device.CHANNELS
        self.FORMAT = self.device.FORMAT
        self.OneSideFFT_points = self.CHUNK/2 + 1      #Calculate the of one-side FFF points.
        self.window = np.ones(self.CHUNK)
				
        self.ON_OFF = False   # False means OFF

        ''' Create Widget for screen'''
        self.ScreenFFT =  Screen.Display("Frequency (Hz)", "Magnitude",  [0,8000], [0,1.5])
        
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
        #global window
		x = {0: np.ones(self.CHUNK), 
				1:  np.hamming(self.CHUNK), 
				2: np.hanning(self.CHUNK), 
				3: np.bartlett(self.CHUNK), 
				4: np.blackman(self.CHUNK)}
		self.window = x[index]
		# if   index == 0:
            # self.window = np.ones(self.CHUNK)
        # elif index == 1:
            # self.window = np.hamming(self.CHUNK)
        # elif index == 2:
            # self.window = np.hanning(self.CHUNK)
        # elif index == 3:
            # self.window = np.bartlett(self.CHUNK)
        # elif index == 4:
             # self.window = np.blackman(self.CHUNK)

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
        #global window
        CH1, CH2 = self.device.readSignal()
        timeSignalCH1 = CH1*self.window
        timeSignalCH2 = CH2*self.window
        TwoSideFFT = np.fft.fft(timeSignalCH1)/ (self.CHUNK)   # Two-side FFT.   We devided by CHUNK (please revise FFT)
        OneSideFFT = 2 * TwoSideFFT[0 : self.OneSideFFT_points]  # we multiply by 2, because we remove the second FFT side (read FFT)
        MagnitudeFFT = np.abs(OneSideFFT)
        #freqSignal_dB = 10*np.log10(freqSignal)
        timeRange = np.arange(0 , self.CHUNK) / float(self.samlingRate)
        freqRange = np.arange(0 , self.OneSideFFT_points) * (float(self.samlingRate)/ float(self.CHUNK))

        return MagnitudeFFT, freqRange

    def plotOnScreen(self):
        MagnitudeFFT, freqRange  = self.calculateFFT()
        self.ScreenFFT.CH1Curve.setData(freqRange, MagnitudeFFT)


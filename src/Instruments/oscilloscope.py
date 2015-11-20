import pyaudio
import numpy as np
import pyqtgraph as pg
from PySide import QtCore, QtGui
#import Devices
import Interface.soundCard as Devices
import Instruments.Screen as Screen

CHUNK = 2048    #  CHUNK is power of 2
samlingRate = 88200 # sampling/second
CHANNELS = 2
FORMAT = pyaudio.paInt16

OneSideFFT_points = CHUNK/2 + 1      #Calculate the of one-side FFF points.
window = np.ones(CHUNK)



''' Oscilloscpe Class ======================================================================='''
class oscilloscope(QtGui.QWidget):
    def __init__(self, parent=None):
        super(oscilloscope, self).__init__(parent)

        self.device =  Devices.sundCardDevice()
        self.CHUNK = self.device.CHUNK    #  CHUNK is power of 2
        self.samlingRate = self.device.samlingRate # sampling/second
        self.CHANNELS = self.device.CHANNELS
        self.FORMAT = self.device.FORMAT
        self.window = np.ones(self.CHUNK)
		
		
        self.ON_OFF = False   # False means OFF

        ''' Create Widget for screen'''
        self.ScreenTIME = Screen.Display("Time (ms)", "Amplitude",  [0 , .022], [-1.5 , 1.5])
        self.timePlotCH1  = self.ScreenTIME.plot(pen='y', )
        self.timePlotCH2  = self.ScreenTIME.plot(pen='r', )
        
        ''' Create list box of Frequency range'''
#         self.FreqRangeGroup = QtGui.QGroupBox("Time Duration (ms)")
#         self.FreRangeLayout = QtGui.QGridLayout()
#         self.SpinBoxStartFreq = QtGui.QDoubleSpinBox()
#         self.SpinBoxStopFreq  = QtGui.QDoubleSpinBox()
#         self.LabelStartFreq = QtGui.QLabel("Start")
#         self.LabelStopFreq  = QtGui.QLabel("Stop")   
#         self.SpinBoxStartFreq.setRange(0,1)
#         # self.SpinBoxStopFreq.setMinimum(0)
#         # self.SpinBoxStopFreq.setMaximum(1000000000)
#         self.SpinBoxStartFreq.setValue(0)
#         self.SpinBoxStopFreq.setValue(.022)
#         self.SpinBoxStartFreq.setSingleStep(0.01)
#         self.SpinBoxStopFreq.setSingleStep(0.01)
#         self.FreRangeLayout.addWidget(self.LabelStartFreq,0,0)
#         self.FreRangeLayout.addWidget(self.LabelStopFreq,1,0)
#         self.FreRangeLayout.addWidget(self.SpinBoxStartFreq,0,1)
#         self.FreRangeLayout.addWidget(self.SpinBoxStopFreq,1,1)
#         self.FreqRangeGroup.setLayout(self.FreRangeLayout)
#         self.SpinBoxStartFreq.valueChanged.connect(self.StartFreqChanged)
#         self.SpinBoxStopFreq.valueChanged.connect(self.StopFreqChanged)
        self.ch1_panel = ChPanel("Ch1")
        self.ch2_panel = ChPanel("Ch2")
        
        self.ch1_panel.amplScale_spinBox.valueChanged.connect(self.ch1_panel.scaleChanged)
        
        
        ''' Create power ON/OFF button '''
        self.BtnPower = QtGui.QPushButton("OFF")
        #self.BtnPower.setStyleSheet('QPushButton {color: red}')  

        ''' Layouts '''
        self.mainLayout = QtGui.QVBoxLayout()       # Main  Layout (Horizontal)

        self.ParameterLayout =  QtGui.QGridLayout() # parameter Laygout Grid
        self.ParameterLayout.setSpacing(10)
#         self.ParameterLayout.addWidget(self.FreqRangeGroup, 0,0)
        self.ParameterLayout.addWidget(self.ch1_panel, 0,1)
        self.ParameterLayout.addWidget(self.ch2_panel, 0,2)
        self.ParameterLayout.addWidget(self.BtnPower, 0,3)

        self.mainLayout.addWidget(self.ScreenTIME)
        self.mainLayout.addLayout(self.ParameterLayout)

        self.setLayout(self.mainLayout )


        #QtCore.QObject.connect(button, QtCore.SIGNAL ('clicked()'), someFunc)
        self.BtnPower.clicked.connect(self.BtnPower_clicked)

#     def StartFreqChanged(self):
# 		xLimit = [self.SpinBoxStartFreq.value() , self.SpinBoxStopFreq.value()]
# 		self.ScreenTIME.setRange(xRange=xLimit)
# 
#     def StopFreqChanged(self):
# 		xLimit = [self.SpinBoxStartFreq.value() , self.SpinBoxStopFreq.value()]
# 		self.ScreenTIME.setRange(xRange=xLimit)


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


    def plotOnScreen(self):
        CH1, CH2 = self.device.readSignal()
        timeSignalCH1 = CH1*self.window
        timeSignalCH2 = CH2*self.window
        timeRange = np.arange(0 , self.CHUNK) / float(self.samlingRate)
        self.timePlotCH1.setData(timeRange, timeSignalCH1)
        self.timePlotCH2.setData(timeRange, timeSignalCH2)

		
class ChPanel(QtGui.QWidget):
    def __init__(self,  GroupName):
        super(ChPanel, self ).__init__()
        self.amplScale_lable   = QtGui.QLabel("volt/Div")
        self.amplPsition_lable = QtGui.QLabel("position")
        
        self.amplScale_spinBox = QtGui.QDoubleSpinBox()
        self.amplScale_spinBox.setRange(1,5)
        self.amplScale_spinBox.setSingleStep(0.5)
        
        self.amplPosition_spinBox = QtGui.QDoubleSpinBox()
        self.amplPosition_spinBox.setRange(-1,1)
        self.amplPosition_spinBox.setSingleStep(0.2)
        self.amplPosition_spinBox.setValue(0)
        
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.addWidget(self.amplScale_lable,0,0)
        self.gridLayout.addWidget(self.amplScale_spinBox,0,1)
        self.gridLayout.addWidget(self.amplPsition_lable,1,0)
        self.gridLayout.addWidget(self.amplPosition_spinBox,1,1)
        
        self.ChGroup = QtGui.QGroupBox(GroupName)
        self.ChGroup.setLayout(self.gridLayout)
        
        self.mainLayout = QtGui.QVBoxLayout()       
        self.mainLayout.addWidget(self.ChGroup)                
        self.setLayout(self.mainLayout )
        
    def scaleChanged(self):
        pass
		
import pyaudio
import numpy as np
import pyqtgraph as pg
from PySide import QtCore, QtGui
#import Devices
import Interface.soundCard as Devices
import Instruments.Screen as Screen
from Cython.Plex.Regexps import Str

''' Oscilloscpe Class ======================================================================='''
class oscilloscope(QtGui.QWidget):
    def __init__(self, parent=None):
        super(oscilloscope, self).__init__(parent)

        self.device =  Devices.sundCardDevice()
        self.CHUNK = self.device.CHUNK    #  CHUNK is power of 2
        self.samlingRate = self.device.samlingRate # sampling/second
        self.CHANNELS = self.device.CHANNELS
        self.FORMAT = self.device.FORMAT
			
        self.ON_OFF = False   # False means OFF

        ''' Create Widget for screen'''
        self.ScreenTIME = Screen.Display("Time (ms)", "Amplitude",  [0 , .022], [-1 , 1])
        
        self.markerPos_label = pg.LabelItem(test = 'rajab   d')
        self.ScreenTIME.addItem(self.markerPos_label)
        
        self.timePlotCH1  = self.ScreenTIME.plot(pen='y', )
        self.timePlotCH2  = self.ScreenTIME.plot(pen='r', )
        
        
        self.marker1 = pg.InfiniteLine(angle=90, movable=True)      # create  Marker1 
        self.ScreenTIME.addItem(self.marker1, ignoreBounds=True)    # add marker to the view
        self.marker1.sigPositionChangeFinished.connect(self.markerChanged) # signal and slote for marker position changed
        
        self.ch1_panel = ChPanel("Ch1")
        self.ch2_panel = ChPanel("Ch2")
        
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
#     def StopFreqChanged(self):
# 		xLimit = [self.SpinBoxStartFreq.value() , self.SpinBoxStopFreq.value()]
# 		self.ScreenTIME.setRange(xRange=xLimit)

    def markerChanged(self):
        PosMarker = self.marker1.value()
        self.markerPos_label.setText("<span style='color: red'>y1=%0.1f</span>" % (PosMarker))
        print PosMarker


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
        timeSignalCH1 = (self.ch1_panel.AmplitudeScaleBy * CH1) + self.ch1_panel.PositionShifBy
        timeSignalCH2 = (self.ch2_panel.AmplitudeScaleBy * CH2) + self.ch2_panel.PositionShifBy
        
        timeRange = np.arange(0 , self.CHUNK) / float(self.samlingRate)
        self.timePlotCH1.setData(timeRange, timeSignalCH1)
        self.timePlotCH2.setData(timeRange, timeSignalCH2)

''' creeate panel control for Channel 1 and channel 2		'''
class ChPanel(QtGui.QWidget):
    def __init__(self,  GroupName):
        super(ChPanel, self ).__init__()
        self.AmplitudeScaleBy = 1
        self.PositionShifBy   = 0
    
        self.amplScale_lable   = QtGui.QLabel("Amplitude X ")
        self.amplPsition_lable = QtGui.QLabel("position")
        
        self.amplScale_spinBox = QtGui.QDoubleSpinBox()
        self.amplScale_spinBox.setRange(0,5)
        self.amplScale_spinBox.setSingleStep(0.5)
        self.amplScale_spinBox.setValue(1)

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
        
        #QtCore.QObject.connect(button, QtCore.SIGNAL ('clicked()'), someFunc)
        self.amplScale_spinBox.valueChanged.connect(self.scaleChanged)
        self.amplPosition_spinBox.valueChanged.connect(self.PositionChanged)
        
    def scaleChanged(self):
        self.AmplitudeScaleBy = self.amplScale_spinBox.value()
        
    def PositionChanged(self):
        self.PositionShifBy = self.amplPosition_spinBox.value()
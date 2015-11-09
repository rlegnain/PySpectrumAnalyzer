import pyaudio
import numpy as np
import pyqtgraph as pg
import PySide 
import Screen

class spectrumAnalyser(PySide.QtGui.QWidget):

	def __initi__ ():
        super(spectrumAnalyser, self).__init__()

        ''' Create screen to plot Frequency domain  '''
        self.ScreenFFT =  Screen.Display("fREQUENCY (Hz)", "Magnitude",  [0,8000], [0,2000])
        self.fftPlot = self.ScreenFFT.plot(pen='y', )

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
        self.screenLyout.addWidget(self.ScreenFFT,)

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

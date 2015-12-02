import pyaudio
import numpy as np
import pyqtgraph as pg
import PySide 
#import Devices
import Interface.soundCard as Devices
from turtle import Pen

class Display(pg.GraphicsLayoutWidget):
	"""docstring for ClassName"""
	def __init__(self, xLabel, yLabel,  xLimit, yLimit):
		super(Display, self).__init__()
		self.view = self.addPlot()     # add plot to show the curves
		self.nextRow()
		self.reading = self.addLabel("marker position: " )  # add lable which used for read parameters
		
		
		''' config view '''
		self.CH1Curve = self.view.plot(pen='r')
		self.CH2Curve = self.view.plot(pen='y')		
		
		self.setBackground( background=(44, 44, 0)) # define plot windows
		self.view.showGrid(x = True, y = True, alpha = 0.3) 
		self.view.setLabels(bottom=xLabel, top='') 
		self.view.setLabels(left=yLabel, right='')
		self.view.setRange(xRange=xLimit)
		self.view.setRange(yRange=yLimit)
		
		'''config reading '''
		
		
		
		
		''' create marker  '''
		self.region = pg.LinearRegionItem(values=[0,0.01])
		self.view.addItem(self.region)
		self.region.sigRegionChangeFinished.connect(self.markerChanged) # signal and slote for marker position changed
		#self.marker1 = pg.InfiniteLine(angle=90, movable=True)	  # create  Marker1 
		#self.ScreenTIME.addItem(self.marker1, ignoreBounds=True)	# add marker to the view
		#self.marker1.sigPositionChangeFinished.connect(self.markerChanged) # signal and slote for marker position changed
	
	def markerChanged(self):
		values = self.region.getRegion()
		self.reading.setText("marker position: " + str(values))
		#values = self.marker1.value()
		#self.markerPos_label.setText("<span style='color: red'>y1=%0.1f</span>" % (values))
		print values

import pyaudio
import numpy as np
import pyqtgraph as pg
import PySide 
import Devices

class Display(pg.PlotWidget):
	"""docstring for ClassName"""
	def __init__(self, xLabel, yLabel,  xLimit, yLimit):
		super(Display, self).__init__()
		self.setBackground( background=(44, 44, 0)) # define plot windows
		self.showGrid(x = True, y = True, alpha = 0.3) 

		self.setLabels(bottom=xLabel) 
		self.setLabels(left=yLabel)
		self.setRange(xRange=xLimit)
		self.setRange(yRange=yLimit)
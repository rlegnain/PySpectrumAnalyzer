from PySide import QtCore, QtGui

class settingUI(QtGui.QWidget):
	def __init__(self, parent=None):
		super(settingUI, self).__init__()

		
		# Create  Label and Spin Box for Inteface 
		self.LabelInterface = QtGui.QLabel("Interface")         # Lablel of Interface
		self.comBoxInterface = QtGui.QComboBox()            # list of interface
		self.comBoxInterface.addItem("Sound Card")
		#self.comBoxInterface.addItem("USB")
		
		#Create Label and Spin Box for sampling Rate 
		self.LabelSampleRate = QtGui.QLabel("Sampling Rate")         
		self.comBoxSamplingRate = QtGui.QComboBox()              
		self.comBoxSamplingRate.addItem("44100")
		self.comBoxSamplingRate.addItem("88200")
		self.comBoxSamplingRate.addItem("96000")
		self.comBoxSamplingRate.currentIndexChanged[int].connect(self.SelectSamplingRate)

		# Create label and Spin  Box for Chunck
		self.LabelChunck = QtGui.QLabel("Chunk")         # Lablel of Interface
		self.comBoxCunck= QtGui.QComboBox()
		self.comBoxCunck.addItem("1024")
		self.comBoxCunck.addItem("2048")
		self.comBoxSamplingRate.currentIndexChanged[int].connect(self.SelectChunck)
		
		# Creat Label and Spin Box for Format
		self.LabelFormat = QtGui.QLabel("Format")
		self.comBoxFormat= QtGui.QComboBox()
		self.comBoxFormat.addItem("16")
		self.comBoxFormat.addItem("32")

		self.GridLayout = QtGui.QGridLayout()                      #Grid Layout		
		self.GridLayout.setSpacing(10)
		self.GridLayout.horizontalSpacing()
		self.GridLayout.addWidget(self.LabelInterface, 0,0)
		self.GridLayout.addWidget(self.comBoxInterface,0,1)
		self.GridLayout.addWidget(self.LabelSampleRate,1,0)
		self.GridLayout.addWidget(self.comBoxSamplingRate,1,1)
		self.GridLayout.addWidget(self.LabelChunck,2,0)
		self.GridLayout.addWidget(self.comBoxCunck,2,1)
		self.GridLayout.addWidget(self.LabelFormat,3,0)
		self.GridLayout.addWidget(self.comBoxFormat,3,1)

		
		self.VLayout = QtGui.QVBoxLayout()
		self.VLayout.addStretch(1)
		self.VLayout.addLayout(self.GridLayout)
		self.VLayout.addStretch(10)
		self.HLayout = QtGui.QHBoxLayout()
		#self.HLayout.addStretch(1)
		self.HLayout.addLayout(self.VLayout)
		self.HLayout.addStretch(1)

		self.setLayout(self.HLayout)
		
		# function
	def SelectSamplingRate (self, index):
		if index=="44100":
			samplingRate = 44100
		elif index=="88200":
			samplingRate = 88200
		elif index=="96000":
			samplingRate = 96000
			
				
	def SelectChunck(self, index):
		if index=="1024":
			samplingRate = 1024
		elif index=="2048":
			samplingRate = 2048
				
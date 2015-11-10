import pyaudio
import numpy as np
import pyqtgraph as pg
import PySide 


class sundCardDevice:
	def __init__(self, FORMAT, CHANNELS, samlingRate, CHUNK):
		self.FORMAT = FORMAT;
		self.CHANNELS = CHANNELS
		self.samlingRate = samlingRate
		self.CHUNK = CHUNK
    
	def openPort(self):   
		self.p = pyaudio.PyAudio()
		self.Stream = self.p.open(format = self.FORMAT, channels = self.CHANNELS, rate = self.samlingRate, input = True, frames_per_buffer = self.CHUNK)

	def readSignal(self):
		signal = self.Stream.read(self.CHUNK)
		data = np.fromstring(signal, dtype=np.int32)
		
		return data[::2] , data[1::2]

	def closePort(self):
		self.Stream.stop_stream()
		self.Stream.close()
		self.p.terminate()
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
		self.maxVal = 2.0**(16-1)    #  (16bit -1bit)  = 15 for scaling the amplitude
	def openPort(self):   
		self.p = pyaudio.PyAudio()
		self.Stream = self.p.open(format = self.FORMAT, channels = self.CHANNELS, rate = self.samlingRate, input = True, frames_per_buffer = self.CHUNK)

	def readSignal(self):
		signal = self.Stream.read(self.CHUNK)
		data = np.fromstring(signal, dtype=np.int16)
		return data[::2]/self.maxVal , data[1::2]/self.maxVal


	def closePort(self):
		self.Stream.stop_stream()
		self.Stream.close()
		self.p.terminate()

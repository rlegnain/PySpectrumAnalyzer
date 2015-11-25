import pyaudio
import numpy

cycle = 1
freq = 440.00   # frequency in Hz
fs = 44100    # sampling rate
N =int(cycle * fs)  # no of sample per cycle
factor = freq * (numpy.pi * 2) / fs
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=1)

sig = numpy.concatenate([numpy.sin( numpy.arange(N) * factor)])
print sig

stream.write(sig.astype(numpy.float32).tostring())

stream.close()
p.terminate()

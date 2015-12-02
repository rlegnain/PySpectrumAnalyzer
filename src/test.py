from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

# initialize the PyQt Gui
app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.resize(800,800)
view = pg.GraphicsLayoutWidget() 
mw.setCentralWidget(view)
mw.show()
mw.setWindowTitle('Wine Plots')


## create four areas to add plots
w1 = view.addPlot(title = "pH vs alcohol in red Wines")
w2 = view.addPlot(title ="pH vs alcohol in white Wines")
view.nextRow()
w3 = view.addPlot(title = "residual Sugar vs Density in red Wines")
w4 = view.addPlot(title = "residual Sugar vs Density in white Wines")
print("Generating data, this takes a few seconds...")

## 1: pH vs Alcohol red wines  (color = quality)
x = np.cos(np.linspace(0, 2*np.pi, 1000))
data = np.sin(np.linspace(0, 4*np.pi, 1000))

c1 = w1.plot(pen="r")
c2 = w1.plot(pen="y")
c1.setData(data)
c2.setData(2*data)

## 2: pH vs Alcohol  white(color = quality)
w2.plot(data)

## 3: pH vs Alcohol  red(color = quality)
w3.plot(data)

## 4: pH vs Alcohol  whites(color = quality)
#w4.addItem(s4)

gl = pg.GradientLegend((10,100),(300,10))
gl.setIntColorScale(0,100)
gl.scale(1,-1)
w4.addItem(gl)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
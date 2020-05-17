from pylab import *
from drawnow import drawnow, figure
from random import randint

y = []

figure()
def plotfunc():
    y.append(randint(0,50))
    x = range(len(y))
    plot(x,y)

for i in range(200):
    drawnow(plotfunc)

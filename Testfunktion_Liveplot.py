from pylab import plot, legend, xlabel, ylabel, plt
from drawnow import drawnow, figure
from random import randint

y = []

figure()
def plotfunc():
    y.append(randint(0,50))
    x = range(len(y))
    line, = plot(x,y)
    plt.title('Diagram XY')
    line.set_label('Label Graph')
    legend()
    xlabel('Time')
    ylabel('Stuff')

for i in range(200):
    drawnow(plotfunc)

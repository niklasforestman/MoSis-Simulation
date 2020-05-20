#Trägt nicht zum Hauptprogramm bei, dient der Demonstration und einfachen Einarbeitung in die
# Funktionsweise des Animation-Plots

from pylab import plot, legend, xlabel, ylabel, plt
from drawnow import drawnow, figure #figure muss aus drawnow importiert werden
from random import randint

y = []


figure() #figure aus drawnow wird erstellt
def plotfunc():
    #ausführbare Funktion, die den Plot erstellt
    y.append(randint(0,50))
    x = range(len(y))
    line, = plot(x,y)
    plt.title('Diagram XY')
    line.set_label('Label Graph')
    legend()
    xlabel('Time')
    ylabel('Stuff')

for i in range(200):
    #drawnow ruft die ausführbare Funktion aus und animiert diese
    drawnow(plotfunc)

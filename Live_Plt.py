from pylab import *
from drawnow import drawnow, figure
import numpy as np

def Live_Plt(people_alive, people_immune, people_infected, people_dead, r0_current):
    drawnow(drawfkt, *[people_alive, people_immune, people_infected, people_dead, r0_current])

def drawfkt(people_alive, people_immune, people_infected, people_dead, r0_current):
    x=np.arange(np.nonzero(people_alive)[0][0], np.nonzero(people_alive)[0][-1]+1)
    y=people_alive[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1]
    plot(x,y)

    x=np.arange(np.nonzero(people_alive)[0][0], np.nonzero(people_alive)[0][-1]+1)
    y=people_immune[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1]
    plot(x,y)

    x=np.arange(np.nonzero(people_alive)[0][0], np.nonzero(people_alive)[0][-1]+1)
    y=people_infected[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1]
    plot(x,y)

    x=np.arange(np.nonzero(people_alive)[0][0], np.nonzero(people_alive)[0][-1]+1)
    y=people_dead[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1]
    plot(x,y)

    x=np.arange(np.nonzero(people_alive)[0][0], np.nonzero(people_alive)[0][-1]+1)
    y=r0_current[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1]
    plot(x,y)

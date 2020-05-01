'''import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np

def Live_Plot(people_alive, people_immune, people_infected, people_dead, fig, ax1):
    x = np.arange(np.nonzero(people_alive)[0][0], np.nonzero(people_alive)[0][-1]+1),
    y = people_alive[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1]
    ani = animation.FuncAnimation(fig, animate, x, y, ax1)
    plt.show()

def animate((x, y, ax1)):
    ax1.clear()
    ax1.plot(x, y)

'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

TWOPI = 2*np.pi

fig, ax = plt.subplots()

t = np.arange(0.0, TWOPI, 0.001)
s = np.sin(t)
l = plt.plot(t, s)

ax = plt.axis([0,TWOPI,-1,1])

redDot, = plt.plot([0], [np.sin(0)], 'ro')

def animate(i):
    redDot.set_data(i, np.sin(i))
    return redDot,

# create animation using the animate() function
myAnimation = animation.FuncAnimation(fig, animate, frames=np.arange(0.0, TWOPI, 0.1), \
                                      interval=10, blit=True, repeat=True)

plt.show()

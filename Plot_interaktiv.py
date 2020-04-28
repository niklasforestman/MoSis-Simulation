import plotly.graph_objs as go
import numpy as np
from plotly.offline import iplot

'''
Plot Funktion kann jetzt flexibler mit Input arbeiten
Vorgehen:
-   Inputs werden auf 0 überprüft (Arrays sind ursprünglich leer und werden im Programm
    teils vollgeschrieben) - Anteile, die 0 enthalten werden entfernt
-   Angepasste Arrays von den vier Kategorien werden gebildet
-   die vier angepassten Arrays bilden die Datengrundlage für den Plot
-   Plot wird erstellt
'''

def Plot_interaktiv(people_alive, people_immune, people_infected, people_dead):

    alive_end = go.Scatter(
        x=np.arange(np.nonzero(people_alive)[0][0], np.nonzero(people_alive)[0][-1]+1),
        y=people_alive[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1],
        name='Alive'
    )
    immune_end = go.Scatter(
        x=np.arange(np.nonzero(people_alive)[0][0], np.nonzero(people_alive)[0][-1]+1),
        y=people_immune[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1],
        name='Immune'
    )
    infected_end = go.Scatter(
        x=np.arange(np.nonzero(people_alive)[0][0], np.nonzero(people_alive)[0][-1]+1),
        y=people_infected[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1],
        name='Infected'
    )
    deceased_end = go.Scatter(
        x=np.arange(np.nonzero(people_alive)[0][0], np.nonzero(people_alive)[0][-1]+1),
        y=people_dead[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1],
        name='Deceased'
    )
    data = [alive_end, immune_end, infected_end, deceased_end]

    layout = go.Layout(
        title=go.layout.Title(
            text='Result'
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text='Days'

            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text='Part of Population'

            )
        )
    )

    fig = go.Figure(data=data, layout=layout)
    iplot(fig)

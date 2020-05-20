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

def Plot_interaktiv(people_alive, people_immune, people_infected, people_dead,r0_current):
    # Funktion ist rechenaufwändig, wird nur zum Ende einmal aufgerufen

    #Erstellen der Datenpunkte für den Plot als Scatter
    alive_end = go.Scatter(
        x=np.arange(np.nonzero(people_alive)[0][0], np.nonzero(people_alive)[0][-1]+1),
        y=people_alive[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1],
        name='Alive',
        line=dict(color='black')
    )
    immune_end = go.Scatter(
        x=np.arange(np.nonzero(people_alive)[0][0], np.nonzero(people_alive)[0][-1]+1),
        y=people_immune[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1],
        name='Immune',
        line=dict(color='#B5E51D')
    )
    infected_end = go.Scatter(
        x=np.arange(np.nonzero(people_alive)[0][0], np.nonzero(people_alive)[0][-1]+1),
        y=people_infected[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1],
        name='Infected',
        line=dict(color='#FEAEC9')
    )
    deceased_end = go.Scatter(
        x=np.arange(np.nonzero(people_alive)[0][0], np.nonzero(people_alive)[0][-1]+1),
        y=people_dead[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1],
        name='Deceased',
        line=dict(color='#FE0000')
    )
    r0_end = go.Scatter(
        x=np.arange(np.nonzero(people_alive)[0][0], np.nonzero(people_alive)[0][-1]+1),
        y=r0_current[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1],
        name='$R_0$',
        line=dict(color='#1F77B4')
    )
    data = [alive_end, immune_end, infected_end, deceased_end,r0_end] #alle Datensätze werden zusammengefasst

    #Formatierung des Plots
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

    #Erstellen und Plotten des Figures
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)

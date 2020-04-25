import plotly.graph_objs as go
import numpy as np
from plotly.offline import iplot

def Plot_interaktiv(people_alive, people_immune, people_infected, people_dead):

    alive_end = go.Scatter(
        x=np.arange(np.where(people_alive == 0)[0][0]),
        y=people_alive[:np.where(people_alive == 0)[0][0]],
        name='Alive'
    )
    immune_end = go.Scatter(
        x=np.arange(np.where(people_alive == 0)[0][0]),
        y=people_immune[:np.where(people_alive == 0)[0][0]],
        name='Immune'
    )
    infected_end = go.Scatter(
        x=np.arange(np.where(people_alive == 0)[0][0]),
        y=people_infected[:np.where(people_alive == 0)[0][0]],
        name='Infected'
    )
    deceased_end = go.Scatter(
        x=np.arange(np.where(people_alive == 0)[0][0]),
        y=people_dead[:np.where(people_alive == 0)[0][0]],
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

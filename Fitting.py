import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import os
import xlrd
import pandas as pd
from timeit import default_timer as timer


def fitting(start,max_days, day_counter, people_immune,people_infected):
    start1 = timer()
    day_counter = day_counter

    days = np.zeros(day_counter)
    days_total = np.zeros(day_counter+30)
    berechnung_people_immune = np.ones(day_counter)
    berechnung_people_infected = np.ones(day_counter)
    for i in range (0,day_counter+30):
        days_total[i] = i+1
    for i in range (0,day_counter):
        days[i] = i+1
        berechnung_people_immune[i] = people_immune[i]
        berechnung_people_infected[i] = people_infected[i]


   #people_immune = people_immune

    #days=np.arange(np.nonzero(people_immune)[0][0], np.nonzero(people_immune)[0][-1]+1),
    #people_immune=people_immune[np.nonzero(people_immune)[0][0]:np.nonzero(people_immune)[0][-1]+1],


    def test_func(days,S,k):

        return ((start*S)/(start+(S-start)*np.exp(-S*k*days)))

    def test_func2(days,a,b,c):
        return (a*np.exp(-(c*days-b)**2))

    #Es werden die parameter der zu fittenden Funktion bestimmt.
    # Dabei werden Unter- und Obergrenzen der jeweiligen Paramter vorgegeben umd das Fitting zu verbessern und zu beschleunigen - Stimmt das?!?
    params1, params_covariance = opt.curve_fit(test_func,days,berechnung_people_immune,p0=[0.66,0.1],bounds=(0, [1., 2]))

    #if day_counter < 30:
    #    print("Achtung: Zu wenige Daten als Grundlage für Fit")

    #print('S: ',params1[0],' k: ',params1[1])

    params2, params_covariance2 = opt.curve_fit(test_func2,days,berechnung_people_infected,p0=[0.2,1,0.01],bounds=(0, [0.5,10, 0.5]))

    #print('a: ',params2[0],' b: ',params2[1],' c: ',params2[2])

    s3 = test_func(days_total,params1[0],params1[1])
    s4 = test_func2(days_total,params2[0],params2[1],params2[2])
    return(s3,s4,days_total)

    """
    fig, ax1 = plt.subplots()

    s1 = berechnung_people_immune
    ax1.plot(days, s1, 'b-')
    ax1.set_xlabel('Days')
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel('Immune', color='b')
    ax1.tick_params('y', colors='b')


    s3 = test_func(days_total,params[0],params[1])
    ax1.plot(days_total, s3, 'g-')
    ax1.set_ylabel('FIT', color='g')
    ax1.tick_params('y', colors='g')


    s2 = berechnung_people_infected
    ax1.plot(days, s2, 'b-')
    ax1.set_xlabel('Days')
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel('Infected', color='b')
    ax1.tick_params('y', colors='b')


    s4 = test_func2(days_total,params2[0],params2[1],params2[2])
    ax1.plot(days_total, s4, 'r-')
    ax1.set_ylabel('FIT', color='r')
    ax1.tick_params('y', colors='r')
    end = timer()
    print(end-start1)
    fig.tight_layout()
    plt.show()"""


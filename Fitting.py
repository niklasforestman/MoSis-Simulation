import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import os
import xlrd
import pandas as pd


def fitting(max_days, day_counter, people_immune):

    day_counter = day_counter

    days = np.zeros(max_days)

    for i in range (0,max_days):
        days[i] = i+1


    #people_immune = people_immune

    #days=np.arange(np.nonzero(people_immune)[0][0], np.nonzero(people_immune)[0][-1]+1),
    #people_immune=people_immune[np.nonzero(people_immune)[0][0]:np.nonzero(people_immune)[0][-1]+1],


    def test_func(days,a,S,k):

        return ((a*S)/(a+(S-a)*np.exp(-S*k*days)))

    #Es werden die parameter der zu fittenden Funktion bestimmt.
    # Dabei werden Unter- und Obergrenzen der jeweiligen Paramter vorgegeben umd das Fitting zu verbessern und zu beschleunigen - Stimmt das?!?
    params, params_covariance = opt.curve_fit(test_func,days,people_immune,p0=[1,1,1])
    print('a: ',params[0],' b: ',params[1],' c: ',params[2])



    fig, ax1 = plt.subplots()

    s1 = people_immune
    ax1.plot(days, s1, 'b-')
    ax1.set_xlabel('Days')
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel('Immune', color='b')
    ax1.tick_params('y', colors='b')

    ax3 = ax1.twinx()
    s3 = test_func(days,params[0],params[1],params[2])
    ax3.plot(days, s3, 'g-')
    ax3.set_ylabel('FIT', color='g')
    ax3.tick_params('y', colors='g')

    fig.tight_layout()
    plt.show()


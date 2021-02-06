import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import os
import xlrd
import pandas as pd
from timeit import default_timer as timer

#Die Fitting-Funktion emöglicht eine Vorhersage über die zukünftige Entwicklung der Infketionslast und der Immunität in der untersuchten Population

def fitting(start,max_days, day_counter, people_immune,people_infected):
    #start1 = timer()
    day_counter = day_counter
    days = np.zeros(day_counter)
    days_total = np.zeros(day_counter+30)
    berechnung_people_immune = np.ones(day_counter)
    berechnung_people_infected = np.ones(day_counter)
    for i in range (0,day_counter+30):
        days_total[i] = i+1 #Erstellt ein Array, mit fotlaufender Anzahl der Tage.
    for i in range (0,day_counter):
        days[i] = i+1
        berechnung_people_immune[i] = people_immune[i] #Erstellt ein sauberes Array ohne die Nullwerte am Ende
        berechnung_people_infected[i] = people_infected[i]



    def test_func(days,S,k):

        return ((start*S)/(start+(S-start)*np.exp(-S*k*days))) #Testfunktion für die Immunen der Population; Ansatz des sigmuiden Wachstums

    def test_func2(days,a,b,c):
        return (a*np.exp(-(c*days-b)**2)) #Testfunktion für die aktuellen Infezierten; Ansatz einer Glockenkurve

    #Es werden die parameter der zu fittenden Funktion bestimmt.
    # Dabei werden Unter- und Obergrenzen der jeweiligen Paramter vorgegeben umd das Fitting zu verbessern und zu beschleunigen - Stimmt das?!?
    params1, params_covariance = opt.curve_fit(test_func,days,berechnung_people_immune,p0=[0.66,0.1],bounds=(0, [1., 2])) #Optmierung der Immunenentwicklung durch Fit mit der Bibliothek scipy

    params2, params_covariance2 = opt.curve_fit(test_func2,days,berechnung_people_infected,p0=[0.2,1,0.01],bounds=(0, [0.5,10, 0.5]))#Optmierung der Infiziertenentwicklung durch Fit mit der Bibliothek scipy

    s3 = test_func(days_total,params1[0],params1[1])
    s4 = test_func2(days_total,params2[0],params2[1],params2[2])
    return(s3,s4,days_total) #Rückgabewerte sind die Arrays s3 = Immune , s4 = Inifzizierte und Tage bei Fit



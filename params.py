import sys
import pygame
import pandas as pd
from pygame.locals import *
from random import randint
import numpy as np
import bisect

class Params:
    
    def __init__(self):

        self.scale = 700 #Standardeinstellung: 700 #Skalierung
        self.up = 1 ##Standardeinstellung: 1  #Bewegungsgeschwindigkeit der Personen
        self.dev_mode = True
        self.result = True
        #Szenario_1: Isolierung aller ab einer bestimmten Infektionszahl
        #Szenario_2: Isolierung von Personen mit Symptomen
        self.events_enabled = 0 # Bei bestimmten Punkten reguliert sich das System probehalber selbst.
        self.isolation_enabled = False #Parameter Definition für die Selbstregulierung
        self.tests_enabled = False
        self.area_grid = 1 # Anzahl voneinander abgegerenzter Bereiche pro Achse (-> Anzahl Bereiche entspricht Quadrat der Zahl)
        self.cross_prob = 10 # Wahrscheinlichkeit eine Grenze bei Erreichen zu Überqueren in Prozent

        if self.scale > 600:
            self.popsize = self.scale + 600
        else:
            self.popsize = self.scale

        self.end_dist = pd.DataFrame(columns=['Age','Alive'],index=range(self.popsize))



        if self.dev_mode == True:
        
            self.isolation = 0 #Standardeinstellung: 0
            self.infected = 2 #Standardeinstellung: 2
            self.infection_chance = 86#Standardeinstellung: 60
            self.recovery = 8 #Standardeinstellung:8
            self.heavy_case = 10#Standardeinstellung: 2
            self.incubation_time = 40 #Standardeinstellung: 20
            self.superspreader = 50 #Standardeinstellung: 10
            self.testrate = 100
        
        else:
            # Game Settings
            print("Please enter an isolation constant (0-100):")
            self.isolation = float(input())
        
            print("Please enter an starting infected population (0-100):")
            self.infected = int(input())
        
            print("Please enter an infection chance (0-100):")
            self.infection_chance = int(input())
        
            #print("Please enter a mortality rate (0-100):")
            #mortality = int(input())
            #über Statistik eingeführt
        
            print("Please enter a recovery rate (0-100):")
            self.recovery = int(input())
        
            print("Please enter a chance of a heavy case (0-100):")
            self.heavy_case = int(input())

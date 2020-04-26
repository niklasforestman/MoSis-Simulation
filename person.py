import sys
import pygame
import pandas as pd
from pygame.locals import *
from random import randint
import numpy as np
import bisect
from Excel_Auswertung import Excel_Auswertung
from Plot_interaktiv import Plot_interaktiv
from params import Params
import _multiprocessing
params = Params()



class Person_Statistics:
    def __init__(self):
        self.pop_dist = [[0,18.4],[20,18.4+24.6],[40,18.4+24.6+28.8],[60,18.4+24.6+28.8+21.7],[80,18.4+24.6+28.8+21.7+6.5]]
        #Altersverteilung in Deutschland nach (https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Bevoelkerungsstand/Tabellen/liste-altersgruppen.html)
        #erster Eintrag: Untergrenze Alter, zweiter Eintrag: kumulierter Anteil an Bevölkerung
        self.mort_rate = [[0,(0+0.2)/2/10],[20,0.2/10],[40,(0.4+1.3)/2/10],[60,(3.6+8)/2/10],[80,14.8/10]]#
        #Sterblichkeitsrate über Alter nach (https://www.dw.com/de/coronavirus-endlich-umfassende-daten-aus-china/a-52421582)
        #Quelle: Chinese Center for Disease Control and Prevention
        #erster Eintrag: Untergrenze Alter, zweiter Eintrag: Sterblichkeitsrate angepasst an Altersverteilung




class Person:
    """Beschreibt eine einzelne Person in der Simulation. Die Person hat verschiedene Attribute, welche unten aufgefhrt sind. Eine Person kann über die
    Funktion Contact mit anderen Personen interagieren"""
    def __init__(self, isolated, sick,immune,heavy,infected,superspread):
        p_stat = Person_Statistics()
        self.counter = 0
        self.alive = True
        self.immune = False
        self.isolated = isolated
        self.infected = infected
        self.sick = sick
        self.heavy = heavy
        self.age = 0
        self.mortality = 0
        self.finished = False #Mit Virus in kontakt gekommen. Wichtig für r0-Berechnung
        self.dead =False
        self.superspread = superspread
        if not params.tests_enabled:
            self.tested = True
        else:
            self.tested = False

        if self.isolated:
            self.speed = [0, 0]

        if not params.tests_enabled:
            if self.superspread:
                self.speed = [params.up*randint(-100, 100) * 0.05,params.up*randint(-100, 100) * 0.05]
            else:
                self.speed = [params.up*randint(-100, 100) * 0.025,params.up*randint(-100, 100) * 0.025]
            if sick:
                self.image = pygame.image.load("red box 2.jpg")
            if immune:
                self.image = pygame.image.load("green square 2.jpg")
            if infected:
                self.image = pygame.image.load("rosa box.jpg")
            if superspread:
                self.image = pygame.image.load("yellow box 2.jpg")
            else:
                self.image = pygame.image.load("black box.jpg")
            self.ps = self.image.get_rect()
            k=int(params.scale/10)
            self.left = randint(1, k)
            self.top = randint(1, k)
            rand_age = randint(0,100)
            for age_class in range(len(p_stat.pop_dist)):
                if rand_age < p_stat.pop_dist[age_class][1]:
                    self.age = p_stat.pop_dist[age_class][0] + randint(0,20)
                    break
            for age_class in range(len(p_stat.mort_rate)-1):
                if self.age >= p_stat.mort_rate[-1][0]:
                    self.mortality = p_stat.mort_rate[-1][1]
                    break
                elif self.age < p_stat.mort_rate[age_class+1][0]:
                    self.mortality =  p_stat.mort_rate[age_class][1]
                    break
        elif params.tests_enabled:
            if self.superspread:
                self.speed = [params.up*randint(-100, 100) * 0.05,params.up*randint(-100, 100) * 0.05]
            else:
                self.speed = [params.up*randint(-100, 100) * 0.025,params.up*randint(-100, 100) * 0.025]
            self.image = pygame.image.load("black box.jpg")
            self.ps = self.image.get_rect()
            k=int(params.scale/10)
            self.left = randint(1, k)
            self.top = randint(1, k)
            rand_age = randint(0,100)
            for age_class in range(len(p_stat.pop_dist)):
                if rand_age < p_stat.pop_dist[age_class][1]:
                    self.age = p_stat.pop_dist[age_class][0] + randint(0,20)
                    break
            for age_class in range(len(p_stat.mort_rate)-1):
                if self.age >= p_stat.mort_rate[-1][0]:
                    self.mortality = p_stat.mort_rate[-1][1]
                    break
                elif self.age < p_stat.mort_rate[age_class+1][0]:
                    self.mortality =  p_stat.mort_rate[age_class][1]
                    break


    def new_step(self):
        """Diese Funktion berechnet den nächsten Zeitschritt. Tests, Bewegung, Krankheitsentwicklung werden hier beschrieben und ausgewertet."""

        a = randint(-100,100) # generiert zwei Zufallszahlen, welche für die Wahrscheinlichkeitsrechnung benötigt werden
        b = randint(-100,100)

        #Testen der Personengruppen:
        if params.tests_enabled:
            if abs(a) < params.testrate and (self.infected or self.sick):
                self.tested = True

        #Berechnung der Geschwindigkeiten einer einzelnen Person für den nächsten Zeitschritt:
        if self.isolated:
            self.speed = [0, 0]

        elif self.alive and self.superspread==0:
            self.speed = [a * 0.04*params.up, b * 0.04*params.up]

        #Entscheidung über den Status (Krankheitsverlauf) einezer einzelnen Person der Population:
        if self.infected and abs(a) < params.incubation_time:
                self.infected = False
                self.sick = True
                if not params.tests_enabled or (params.tests_enabled and self.tested):
                    self.image = pygame.image.load("red box 2.jpg")

        #Beschreibt den Heilungsprozess
        if self.sick or self.heavy:
            if abs(b) < params.recovery:
                self.finished = True
                self.isolated = False
                self.sick = False
                self.heavy = False
                self.immune = True
                if not params.tests_enabled or (params.tests_enabled and self.tested):
                    self.image = pygame.image.load("green square 2.jpg")

        if self.sick and abs(a) < params.heavy_case:
            self.isolated = True #Person wird stationär aufgenommen --> Mobilität = 0
            self.superspread = False
            self.heavy = True
            if not params.tests_enabled or (params.tests_enabled and self.tested):
                    self.image = pygame.image.load("red box 2.jpg")

        if self.heavy and abs(a) < self.mortality:
            self.finished = True
            self.alive = False
            self.heavy = False
            self.immune = False
            self.dead = True
            self.sick = False
            #self.immune = False
            self.image = pygame.image.load("dark red 2.jpg")

        if not self.alive:
            self.immune = False


    def contact(self, other): #Laufzeit: ca 4,5 Sekunden
        """ Dies ist eine Funktion, welche den Kontakt zweier Personen beschreibt und die Ansteckungsgefahr simuliert"""
        if self.ps.colliderect(other.ps) and not self.immune and not other.immune and self.alive and other.alive:

            if (self.sick or self.infected or self.heavy) and not (other.sick or other.infected):
                if self.isolated or other.isolated:
                    chance = 2*randint(0,100)
                else:
                    chance = randint(0,100)
                    if params.infection_chance/2 > chance:
                        self.counter +=1 # Zählt die angesteckten Personen durch die Person selbst.
                        other.infected = True
                        if not params.tests_enabled or (params.tests_enabled and self.tested): #Personen, welche durch Infizierte angesteckt werden, werden wie bereits geteste behandelt
                            other.image = pygame.image.load("rosa box.jpg")


    '''def contact(self, other): #Laufzeit: ca 4,5 Sekunden
        """ Dies ist eine Funktion, welche den Kontakt zweier Personen beschreibt und die Ansteckungsgefahr simuliert"""
        if self.ps.colliderect(other.ps) and not self.immune and not other.immune and self.alive and other.alive:

            self.speed[0], self.speed[1] = self.speed[0] * -1, self.speed[1] * -1
            other.speed[0], other.speed[1] = other.speed[0] * -1, other.speed[1] * -1

            if self.sick and not other.sick:
                if params.infection_chance > randint(0,100):
                    self.counter +=1 # Zählt die angesteckten Personen durch die Person selbst.
                    other.infected = True
                    if not params.tests_enabled or (params.tests_enabled and self.tested): #Personen, welche durch Infizierte angesteckt werden, werden wie bereits geteste behandelt
                        other.image = pygame.image.load("rosa box.jpg")

            elif not self.sick and other.sick:
                if params.infection_chance >  randint(0,100):
                    self.infected = True
                    if not params.tests_enabled or (params.tests_enabled and other.tested):
                        self.image = pygame.image.load("rosa box.jpg")

            if self.infected and not other.sick:
                if params.infection_chance > randint(0,100):
                    self.counter +=1
                    other.infected = True
                    if not params.tests_enabled or (params.tests_enabled and self.tested):
                        other.image = pygame.image.load("rosa box.jpg")
            elif not self.sick and other.infected:
                if params.infection_chance >  randint(0,100):
                    self.infected = True
                    if not params.tests_enabled or (params.tests_enabled and other.tested):
                        self.image = pygame.image.load("rosa box.jpg")'''




    '''def contact(self, other): #Laufzeit --> ca 8-10 Sekunden
        """ Dies ist eine Funktion, welche den Kontakt zweier Personen beschreibt und die Ansteckungsgefahr simuliert"""
        if self.ps.colliderect(other.ps) and not self.immune and not other.immune and not self.isolated and not other.isolated and self.alive and other.alive:

            self.speed[0], self.speed[1] = self.speed[0] * -1, self.speed[1] * -1
            other.speed[0], other.speed[1] = other.speed[0] * -1, other.speed[1] * -1

            if self.sick and not other.sick:
                if params.infection_chance > randint(0,100):
                    self.counter +=1 # Zählt die angesteckten Personen durch die Person selbst.
                    other.infected = True
                    if not params.tests_enabled or (params.tests_enabled and self.tested): #Personen, welche durch Infizierte angesteckt werden, werden wie bereits geteste behandelt
                        other.image = pygame.image.load("rosa box.jpg")

            elif not self.sick and other.sick:
                if params.infection_chance >  randint(0,100):
                    self.infected = True
                    if not params.tests_enabled or (params.tests_enabled and other.tested):
                        self.image = pygame.image.load("rosa box.jpg")

            if self.infected and not other.sick:
                if params.infection_chance > randint(0,100):
                    self.counter +=1
                    other.infected = True
                    if not params.tests_enabled or (params.tests_enabled and self.tested):
                        other.image = pygame.image.load("rosa box.jpg")
            elif not self.sick and other.infected:
                if params.infection_chance >  randint(0,100):
                    self.infected = True
                    if not params.tests_enabled or (params.tests_enabled and other.tested):
                        self.image = pygame.image.load("rosa box.jpg")


        if self.ps.colliderect(other.ps) and not self.immune and not other.immune and self.alive and other.alive:

            self.speed[0], self.speed[1] = self.speed[0] * -1, self.speed[1] * -1
            other.speed[0], other.speed[1] = other.speed[0] * -1, other.speed[1] * -1

            if self.sick and not other.sick:
                if params.infection_chance/2 > randint(0,100):
                    self.counter +=1
                    other.infected = True
                    if not params.tests_enabled or (params.tests_enabled and self.tested):
                        other.image = pygame.image.load("rosa box.jpg")
            elif not self.sick and other.sick:
                if params.infection_chance/2 > randint(0,100):
                    self.infected = True
                    if not params.tests_enabled or (params.tests_enabled and other.tested):
                        self.image = pygame.image.load("rosa box.jpg")

            if self.infected and not other.sick:
                if params.infection_chance/2 > randint(0,100):
                    self.counter +=1
                    other.infected = True
                    if not params.tests_enabled or (params.tests_enabled and self.tested):
                        other.image = pygame.image.load("rosa box.jpg")
            elif not self.sick and other.infected:
                if params.infection_chance/2 >  randint(0,100):
                    self.infected = True
                    if not params.tests_enabled or (params.tests_enabled and other.tested):
                        self.image = pygame.image.load("rosa box.jpg")'''


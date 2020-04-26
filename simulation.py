"""
Program: Coronavirus Simulation
Origin Author: Nathan Verghis

New Program Name
Authors: KT MoSi (Albrecht Pohl, Niklas Waldmann)


"""

# Colorcode:
# - Schwarz: Unbekannt
# - Grün: Immun
# - Rosa: Infiziert
# - Rot: Krank
# - Dunkelrot: Verstorben
# - Gelb: Superspreader

#   === INIT ===

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

#Initialisierung der Arrays für die Speicherung der Ergebnisse der einzenen Zeitschritte
days = np.ones(100)
days[0] = 0
people_infected = np.zeros(1000)
darkfigure = np.zeros(1000)
people_immune = np.zeros(1000)
people_dead = np.zeros(1000)
people_alive = np.zeros(1000)
r0_current = np.zeros(1000)
r0_current_superspreader = np.zeros(1000)

#mortality = 2
#params.recovery = 15

pygame.init()
params = Params()
pygame.display.set_caption("Coronavirus Infection Simulation")
size = width, height = params.scale, params.scale
speed = [25, 0]
white = 255, 255, 255
day_counter = 0
count = 0
pop_dist = [[0,18.4],[20,18.4+24.6],[40,18.4+24.6+28.8],[60,18.4+24.6+28.8+21.7],[80,18.4+24.6+28.8+21.7+6.5]]
#Altersverteilung in Deutschland nach (https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Bevoelkerungsstand/Tabellen/liste-altersgruppen.html)
#erster Eintrag: Untergrenze Alter, zweiter Eintrag: kumulierter Anteil an Bevölkerung
mort_rate = [[0,(0+0.2)/2/10],[20,0.2/10],[40,(0.4+1.3)/2/10],[60,(3.6+8)/2/10],[80,14.8/10]]#
#Sterblichkeitsrate über Alter nach (https://www.dw.com/de/coronavirus-endlich-umfassende-daten-aus-china/a-52421582)
#Quelle: Chinese Center for Disease Control and Prevention
#erster Eintrag: Untergrenze Alter, zweiter Eintrag: Sterblichkeitsrate angepasst an Altersverteilung

if params.area_grid > 1: #Grenzen erstellen
    grids = []
    for counter_grid in range(1, params.area_grid):
        grids.append(counter_grid * width / params.area_grid)

# === DEF ===

# Creating People object
class Person:
    """Beschreibt eine einzelne Person in der Simulation. Die Person hat verschiedene Attribute, welche unten aufgefhrt sind. Eine Person kann über die
    Funktion Contact mit anderen Personen interagieren"""
    def __init__(self, isolated, sick,immune,heavy,infected,superspread):
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
            for age_class in range(len(pop_dist)):
                if rand_age < pop_dist[age_class][1]:
                    self.age = pop_dist[age_class][0] + randint(0,20)
                    break
            for age_class in range(len(mort_rate)-1):
                if self.age >= mort_rate[-1][0]:
                    self.mortality = mort_rate[-1][1]
                    break
                elif self.age < mort_rate[age_class+1][0]:
                    self.mortality =  mort_rate[age_class][1]
                    break
        elif params.tests_enabled:
            if self.superspread:
                self.speed = [up*randint(-100, 100) * 0.05,up*randint(-100, 100) * 0.05]
            else:
                self.speed = [up*randint(-100, 100) * 0.025,up*randint(-100, 100) * 0.025]
            self.image = pygame.image.load("black box.jpg")
            self.ps = self.image.get_rect()
            k=int(params.scale/10)
            self.left = randint(1, k)
            self.top = randint(1, k)
            rand_age = randint(0,100)
            for age_class in range(len(pop_dist)):
                if rand_age < pop_dist[age_class][1]:
                    self.age = pop_dist[age_class][0] + randint(0,20)
                    break
            for age_class in range(len(mort_rate)-1):
                if self.age >= mort_rate[-1][0]:
                    self.mortality = mort_rate[-1][1]
                    break
                elif self.age < mort_rate[age_class+1][0]:
                    self.mortality =  mort_rate[age_class][1]
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



    def contact(self, other):
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
                        self.image = pygame.image.load("rosa box.jpg")


def sim_continue(pop):
    """Diese Funktion beschreibt die Endbedingung für das Programm"""
    all_dead = all(not people.alive for people in pop)
    all_healed = all(not people.sick and not people.infected for people in pop)
    return not(all_dead or all_healed)


def statistics(pop):
    """Stellt eine Statistik zusammen, welche am Ende des Programms durchgeführt wird."""
    alive = 0
    dead = 0
    immune = 0

    ppl_count = -1
    for people in pop:
        ppl_count += 1
        params.end_dist['Age'][ppl_count] = people.age
        if people.immune:
            immune+=1
        if people.alive:
            alive += 1
            params.end_dist['Alive'][ppl_count] = 1
        else:
            dead += 1
            params.end_dist['Alive'][ppl_count] = 0

    return alive, dead, immune, params.end_dist




# === PROGRAM ===

screen = pygame.display.set_mode(size)
population = []

# Aufbauen der Population
for i in range(params.popsize):
    is_isolated = False
    is_infected = False
    is_immune = False
    is_heavy = False
    is_superspread = False
    temp = randint(1, params.popsize)
    if temp < params.isolation:
        is_isolated = True # Mit einer gewählten Wahrscheinlichkeit ist die Person isoliert.
    if temp < params.infected:
        is_infected = True # Mit einer gewählten Wahrscheinlichkeit ist die Person infiziert.
    if temp < params.superspreader:
        is_superspread = True  # Mit einer gewählten Wahrscheinlichkeit ist die Person superspreader.
    new_person = Person(is_isolated, is_infected,is_immune,is_heavy,is_infected,is_superspread) #Erstellen eines Objekts Person mit den oben genannten Eigenschaften
    params.end_dist['Age'][i] = new_person.age
    new_person.ps = new_person.ps.move(new_person.left*10, new_person.top*10) # Setzen der Personen auf das Spielfeld
    population.append(new_person)

people_infected[0] = params.infected/params.popsize

# Creating the Simulation
while sim_continue(population):
    count += 1
    if count == 12:
        day_counter += 1



    #Hilfsvariablen für die Berechnung
    inf=0
    inf_2 = 0
    imm=0
    dead=0
    d=0
    fin =0
    d2 = 0
    z2 = 0
    tested = 0

    #Durchzählen der Population auf bestimmte Eigenschaften
    for people in population:
        if people.infected ==True:
            inf+=1
        if (people.infected or people.sick or people.finished) and people.tested:
            inf_2+=1
        if people.sick == True:
            inf+=1
        if people.immune ==True:
            imm +=1
        if people.alive == False:
            dead +=1
        if people.finished:
            fin +=1
            d+= people.counter
        if people.tested:
            tested +=1

    if fin>0:
        r0_current[day_counter] = d/fin
    else:
        r0_current[day_counter] = 0

    people_infected[day_counter]=inf/params.popsize
    if inf_2==0:
        darkfigure[day_counter] = 0
    else:
        darkfigure[day_counter] = (inf+fin)/inf_2
    people_immune[day_counter]=imm/params.popsize
    people_dead[day_counter]=dead/params.popsize
    people_alive[day_counter]=1-dead/params.popsize

    if count == 12:
        print("Tag: ",day_counter,".....","Isolationsaufruf: ",params.isolation_enabled,".....","r0: ", \
              round(r0_current[day_counter],4),".....","aktuell Infizierte: ", round(people_infected[day_counter],4), \
              ".....","Dunkelziffer: ",round(darkfigure[day_counter],3),".....","aktuell Immune: ", \
              round(people_immune[day_counter],4),".....","aktuell Verstorbene: ",round(people_dead[day_counter],4))
        count = 0

    #params.isolation ist während des Programms über die Pfeiltasten rechts und links steuerbar.
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_RIGHT:
            for people in population:
                if randint(0,100)<60:  #Mit einer Wahrscheinlihckeit von 60% halten sich die Personen an die Regeln
                    people.isolated = True
        elif event.type == KEYDOWN and event.key == K_LEFT:
            for people in population:
                if not people.heavy or people.alive:
                    people.isolated = False
                    params.isolation_enabled = False
                    #events_enabled = False #Stellt eigenständige Events aus
     #Impfstoff sofort für alle Kranken verfügbar
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_UP:
            for people in population:
                if people.sick or people.infected:
                    people.sick = False
                    people.infected = False
                    people.immune = True
                    self.image = pygame.image.load("green square 2.jpg")



    if params.events_enabled == 1:
        if people_infected[day_counter] > 0.10 and not params.isolation_enabled:
            for people in population:
                if randint(0,100)<40:  #Mit einer Wahrscheinlihckeit von 40% halten sich die Personen an die Regeln
                    people.isolated = True
                params.isolation_enabled = True
        elif people_infected[day_counter] < 0.05:
            params.isolation_enabled = False
            for people in population:
                if not people.heavy or people.alive:
                    people.isolated = False
    if params.events_enabled == 2:
        for people in population:
            if people.sick:
                people.isolated = True
            elif people.immune:
                people.isolated = False

    screen.fill(white)
    for person in population:
        if 'grids' in globals(): # Grenzen existieren
            #Grenzen zeichnen
            for i in range(len(grids)):
                pygame.draw.line(screen, (0,0,0),(0,grids[i]), (width,grids[i]))
                pygame.draw.line(screen, (0,0,0),(grids[i],0), (grids[i], height))

            # Grenzen funktionieren, aber Probleme mit Figuren, die in Grenznähe bleiben, wenn stochastische Bewegung sie über Grenze führen würde, aber Wahrscheinlichkeit nicht erreicht wird

            # Koordinate 1
            if (bisect.bisect_left(grids, person.ps.move(person.speed)[0]) != bisect.bisect_left(grids, person.ps[0])) \
                & (bisect.bisect_left(grids, person.ps.move(person.speed)[0]*-1) == bisect.bisect_left(grids, person.ps[0])):
                # Person überschreitet Grenze bei Vorwärtsbewegeung, aber nicht bei Rückwärtsbewegung
                if randint(0,100) > params.cross_prob:
                    person.speed[0] = person.speed[0] * -1
            elif (bisect.bisect_left(grids, person.ps.move(person.speed)[0]) != bisect.bisect_left(grids, person.ps[0])) \
                & (bisect.bisect_left(grids, person.ps.move(person.speed)[0]*-1) != bisect.bisect_left(grids, person.ps[0])):
                # Person überschreitet Grenze bei Vorwärts- und Rückwärtsbewegung
                if randint(0,100) > params.cross_prob:
                    person.speed[0] = 0

            # Koordinate 2
            if (bisect.bisect_left(grids, person.ps.move(person.speed)[1]) != bisect.bisect_left(grids, person.ps[1])) \
                & (bisect.bisect_left(grids, person.ps.move(person.speed)[1]*-1) == bisect.bisect_left(grids, person.ps[1])):
                # Person überschreitet Grenze bei Bewegeung, aber nicht bei Rückwärtsbewegung
                if randint(0,100) > params.cross_prob:
                    person.speed[1] = person.speed[1] * -1
            elif (bisect.bisect_left(grids, person.ps.move(person.speed)[1]) != bisect.bisect_left(grids, person.ps[1])) \
                & (bisect.bisect_left(grids, person.ps.move(person.speed)[1]*-1) != bisect.bisect_left(grids, person.ps[1])):
                # Person überschreitet Grenze bei Vorwärts- und Rückwärtsbewegung
                if randint(0,100) > params.cross_prob:
                    person.speed[1] = 0

        person.ps = person.ps.move(person.speed)
        if person.ps.left < 0 or person.ps.right > width:
            person.speed[0] = person.speed[0] * -1
        if person.ps.top < 0 or person.ps.bottom > height:
            person.speed[1] = person.speed[1] * -1
        for friend in population:
            if person is friend:
                pass
            else:
                person.contact(friend)
        if count == 0:
            person.new_step()
        screen.blit(person.image, person.ps)

    pygame.display.flip()



print("Days til completion: ", day_counter)

alive, dead, immune, end_dist = statistics(population)
#stats = statistics(population)
print("Alive: ", alive)
print("Dead: ", dead)
print("Immune: ",immune)


if params.result == True:
    # === AUSWERTUNG ===
    Auswertung_Excel = True
    if Auswertung_Excel:
        Excel_Auswertung (r0_current,people_infected, darkfigure, people_immune, people_dead)

    Plot_interaktiv(people_alive, people_immune, people_infected, people_dead)

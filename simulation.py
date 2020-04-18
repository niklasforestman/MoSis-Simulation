"""
Program: Coronavirus Simulation
Origin Author: Nathan Verghis

New Program Name
Authors: KT MoSi (Albrecht Pohl, Niklas Waldmann)


"""

#BETA - EXcel-Auswertung

#   === INIT ===

import sys
import pygame
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pygame.locals import *
from random import randint
import time
import numpy as np
scale = 700 #Standardeinstellung: 700 #Skalierung
up = 1 ##Standardeinstellung: 1  #Bewegungsgeschwindigkeit der Personen
dev_mode = True
result = True
#Szenario_1: Isolierung aller ab einer bestimmten Infektionszahl
#Szenario_2: Isolierung von Personen mit Symptomen
events_enabled = 0 # Bei bestimmten Punkten reguliert sich das System probehalber selbst.
isolation_enabled = False #Parameter Definition für die Selbstregulierung
tests_enabled = False

if scale > 600:
    popsize = scale + 600
else:
    popsize = scale

end_dist = pd.DataFrame(columns=['Age','Alive'],index=range(popsize))



if dev_mode == True:

    isolation = 0 #Standardeinstellung: 0
    infected = 2 #Standardeinstellung: 2
    infection_chance = 40#Standardeinstellung: 60
    recovery = 12 #Standardeinstellung:8
    heavy_case = 10#Standardeinstellung: 2
    incubation_time = 28 #Standardeinstellung: 20
    superspreader = 50 #Standardeinstellung: 10
    testrate = 100

else:
    # Game Settings
    print("Please enter an isolation constant (0-100):")
    isolation = float(input())

    print("Please enter an starting infected population (0-100):")
    infected = int(input())

    print("Please enter an infection chance (0-100):")
    infection_chance = int(input())

    #print("Please enter a mortality rate (0-100):")
    #mortality = int(input())
    #über Statistik eingeführt

    print("Please enter a recovery rate (0-100):")
    recovery = int(input())

    print("Please enter a chance of a heavy case (0-100):")
    heavy_case = int(input())


#mortality = 2
#recovery = 15

pygame.init()
pygame.display.set_caption("Coronavirus Infection Simulation")
size = width, height = scale, scale
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

# === DEF ===

# Creating People object
class Person:
    """BEschreibt eine einzelne Person in der Simulation. Die Person hat verschiedene Attribute, welche unten aufgefhrt sind. Eine Person kann über die
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
        if not tests_enabled:
            self.tested = True
        else:
            self.tested = False

        if self.isolated:
            self.speed = [0, 0]

        if not tests_enabled:
            if self.superspread:
                self.speed = [randint(-100, 100) * 0.05, randint(-100, 100) * 0.05]
            else:
                self.speed = [randint(-100, 100) * 0.025, randint(-100, 100) * 0.025]
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
            k=int(scale/10)
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
        elif tests_enabled:
            if self.superspread:
                self.speed = [randint(-100, 100) * 0.05, randint(-100, 100) * 0.05]
            else:
                self.speed = [randint(-100, 100) * 0.025, randint(-100, 100) * 0.025]
            self.image = pygame.image.load("black box.jpg")
            self.ps = self.image.get_rect()
            k=int(scale/10)
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
        if tests_enabled:
            if abs(a) < testrate and (self.infected or self.sick):
                self.tested = True

        #Berechnung der Geschwindigkeiten einer einzelnen Person für den nächsten Zweitschritt:
        if self.isolated:
            self.speed = [0, 0]

        elif self.alive and self.superspread==0:
            self.speed = [a * 0.04*up, b * 0.04*up]

        #Entscheidung über den Status (Krankheitsverlauf) einezer einzelnen Person der Population:
        if self.infected and abs(a) < incubation_time:
                self.infected = False
                self.sick = True
                if not tests_enabled or (tests_enabled and self.tested):
                    self.image = pygame.image.load("red box 2.jpg")

        #Beschreibt den Heilungsprozess
        if self.sick or self.heavy:
            if abs(b) < recovery:
                self.finished = True
                self.isolated = False
                self.sick = False
                self.heavy = False
                self.immune = True
                if not tests_enabled or (tests_enabled and self.tested):
                    self.image = pygame.image.load("green square 2.jpg")

        if self.sick and abs(a) < heavy_case:
            self.isolated = True #Person wird stationär aufgenommen --> Mobilität = 0
            self.superspread = False
            self.heavy = True
            if not tests_enabled or (tests_enabled and self.tested):
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
                if infection_chance > randint(0,100): 
                    self.counter +=1 # Zählt die angesteckten Personen durch die Person selbst.
                    other.infected = True 
                    if not tests_enabled or (tests_enabled and self.tested): #Personen, welche durch Infizierte angesteckt werden, werden wie bereits geteste behandelt
                        other.image = pygame.image.load("rosa box.jpg")
                        
            elif not self.sick and other.sick:
                if infection_chance >  randint(0,100):
                    self.infected = True
                    if not tests_enabled or (tests_enabled and other.tested):
                        self.image = pygame.image.load("rosa box.jpg")

            if self.infected and not other.sick:
                if infection_chance > randint(0,100):
                    self.counter +=1
                    other.infected = True
                    if not tests_enabled or (tests_enabled and self.tested):
                        other.image = pygame.image.load("rosa box.jpg")
            elif not self.sick and other.infected:
                if infection_chance >  randint(0,100):
                    self.infected = True
                    if not tests_enabled or (tests_enabled and other.tested):
                        self.image = pygame.image.load("rosa box.jpg")
                        
                        
        if self.ps.colliderect(other.ps) and not self.immune and not other.immune and self.alive and other.alive:
            
            self.speed[0], self.speed[1] = self.speed[0] * -1, self.speed[1] * -1
            other.speed[0], other.speed[1] = other.speed[0] * -1, other.speed[1] * -1
            
            if self.sick and not other.sick:
                if infection_chance/2 > randint(0,100):
                    self.counter +=1
                    other.infected = True
                    if not tests_enabled or (tests_enabled and self.tested):
                        other.image = pygame.image.load("rosa box.jpg")
            elif not self.sick and other.sick:
                if infection_chance/2 > randint(0,100):
                    self.infected = True
                    if not tests_enabled or (tests_enabled and other.tested):
                        self.image = pygame.image.load("rosa box.jpg")

            if self.infected and not other.sick:
                if infection_chance/2 > randint(0,100):
                    self.counter +=1
                    other.infected = True
                    if not tests_enabled or (tests_enabled and self.tested):
                        other.image = pygame.image.load("rosa box.jpg")
            elif not self.sick and other.infected:
                if infection_chance/2 >  randint(0,100):
                    self.infected = True
                    if not tests_enabled or (tests_enabled and other.tested):
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
        end_dist['Age'][ppl_count] = people.age
        if people.immune:
            immune+=1
        if people.alive:
            alive += 1
            end_dist['Alive'][ppl_count] = 1
        else:
            dead += 1
            end_dist['Alive'][ppl_count] = 0

    return alive, dead, immune, end_dist


# === PROGRAM ===

screen = pygame.display.set_mode(size)
population = []

# Aufbauen der Population
for i in range(popsize):
    is_isolated = False
    is_infected = False
    is_immune = False
    is_heavy = False
    is_superspread = False
    temp = randint(1, popsize)
    if temp < isolation: 
        is_isolated = True # Mit einer gewählten Wahrscheinlichkeit ist die Person isoliert.
    if temp < infected:
        is_infected = True # Mit einer gewählten Wahrscheinlichkeit ist die Person infiziert.
    if temp < superspreader:
        is_superspread = True  # Mit einer gewählten Wahrscheinlichkeit ist die Person superspreader.
    new_person = Person(is_isolated, is_infected,is_immune,is_heavy,is_infected,is_superspread) #Erstellen eines Objekts Person mit den oben genannten Eigenschaften
    end_dist['Age'][i] = new_person.age
    new_person.ps = new_person.ps.move(new_person.left*10, new_person.top*10) # Setzen der Personen auf das Spielfeld
    population.append(new_person)


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
people_infected[0] = infected/popsize
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

    people_infected[day_counter]=inf/popsize
    if inf_2==0:
        darkfigure[day_counter] = 0
    else:
        darkfigure[day_counter] = (inf+fin)/inf_2
    people_immune[day_counter]=imm/popsize
    people_dead[day_counter]=dead/popsize
    people_alive[day_counter]=1-dead/popsize

    if count == 12:
        print("Tag: ",day_counter,".....","Isolationsaufruf: ",isolation_enabled,".....","r0: ",r0_current[day_counter],".....","aktuell Infizierte: ",people_infected[day_counter],".....","Dunkelziffer: ",darkfigure[day_counter],".....","aktuell Immune: ",people_immune[day_counter],".....","aktuell Verstorbene: ",people_dead[day_counter])
        count = 0

    #Isolation ist während des Programms über die Pfeiltasten rechts und links steuerbar.
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_RIGHT:
            for people in population:
                if randint(0,100)<60:  #Mit einer Wahrscheinlihckeit von 60% halten sich die Personen an die Regeln
                    people.isolated = True
        elif event.type == KEYDOWN and event.key == K_LEFT:
            for people in population:
                if not people.heavy or people.alive:
                    people.isolated = False
                    isolation_enabled = False
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



    if events_enabled == 1:
        if people_infected[day_counter] > 0.10 and not isolation_enabled:
            for people in population:
                if randint(0,100)<40:  #Mit einer Wahrscheinlihckeit von 40% halten sich die Personen an die Regeln
                    people.isolated = True
                isolation_enabled = True
        elif people_infected[day_counter] < 0.05:
            isolation_enabled = False
            for people in population:
                if not people.heavy or people.alive:
                    people.isolated = False
    if events_enabled == 2:
        for people in population:
            if people.sick:
                people.isolated = True
            elif people.immune:
                people.isolated = False

    screen.fill(white)
    for person in population:
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


if result == True:
    # === AUSWERTUNG ===

    plt.ylabel('Aktuell Infizierte')

    # Einen x-y-Plot erstellen:
    plt.plot(people_infected, 'b-')
    plt.plot(people_immune, 'g-')
    plt.plot(people_dead, 'r-')
    plt.plot(people_alive, 'y-')
    plt.plot(r0_current, 'g-')

    # Achsen-Bereiche manuell festlegen
    # Syntax: plt.axis([xmin, xmax, ymin, ymax])
    #plt.axis([0, 5, 0, 20])

    # Ein gepunktetes Diagramm-Gitter einblenden:
    plt.grid(True)

    # Diagramm anzeigen:
    plt.show()

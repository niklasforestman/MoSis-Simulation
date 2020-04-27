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
from person import Person
from person import Person_Statistics
from statistics import statistics

# === FUNKTIONEN ===
def sim_continue(pop):
    """Diese Funktion beschreibt die Endbedingung für das Programm"""
    all_dead = all(not people.alive for people in pop)
    all_healed = all(not people.sick and not people.infected for people in pop)
    return not(all_dead or all_healed)


# === INITIALISIERUNG von Paramtern ===
#Initialisierung der Arrays für die Speicherung der Ergebnisse der einzenen Zeitschritte
days = np.ones(100)
days[0] = 0
max_days = 300
people_infected = np.zeros(max_days)
darkfigure = np.zeros(max_days)
people_immune = np.zeros(max_days)
people_dead = np.zeros(max_days)
people_alive = np.zeros(max_days)
r0_current = np.zeros(max_days)
r0_current_superspreader = np.zeros(max_days)

# === Init pygame ===
pygame.init()
params = Params()
pygame.display.set_caption("Coronavirus Infection Simulation")
size = width, height = params.scale, params.scale
speed = [25, 0]
white = 255, 255, 255
day_counter = 0
count = 0

if params.area_grid > 1: #Grenzen erstellen
    grids = []
    for counter_grid in range(1, params.area_grid):
        grids.append(counter_grid * width / params.area_grid)



# === PROGRAM ===
if __name__ == "__main__":
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
            elif (event.type == KEYDOWN and event.key == K_UP):
                for people in population:
                    if people.sick or people.infected:
                        people.sick = False
                        people.infected = False
                        people.immune = True
                        people.image = pygame.image.load("green square 2.jpg")

        '''if day_counter == max_days-1:
                for people in population:
                   if people.sick or people.infected:
                        people.sick = False
                        people.infected = False
                        people.immune = True
                        people.image = pygame.image.load("green square 2.jpg")'''


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
        clickPauseEvent(event, population)
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

    if params.result == True:
        statistics(population,params,day_counter)
        # === AUSWERTUNG ===
        Auswertung_Excel = True
        if Auswertung_Excel:
            Excel_Auswertung (r0_current,people_infected, darkfigure, people_immune, people_dead)

        Plot_interaktiv(people_alive, people_immune, people_infected, people_dead)

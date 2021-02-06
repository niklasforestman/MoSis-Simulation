#VERSION 0.3

"""
Program: Coronavirus Simulation
Origin Author: Nathan Verghis, github.com/nathan-verghis

MoSi Coronavirus Simulation
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
import multiprocessing
from timeit import default_timer as timer
from Fitting import fitting
from ClickInteraktion import clickPauseEvent
from multiprocessing import Process, Queue
import GUI
from ini import *
from pylab import plot, legend, xlabel, ylabel, plt, ylim
from drawnow import drawnow, figure


# === FUNKTIONEN ===
def sim_continue(pop):
    """Diese Funktion beschreibt die Endbedingung für das Programm"""
    all_dead = all(not people.alive for people in pop)
    all_healed = all(not people.sick and not people.infected for people in pop)
    return not(all_dead or all_healed)

def drawfkt():
    # Enthält die Befehle für den Liveplot, wird über Animationsfunktion aufgerufen
    #Teil für den Fit

    if day_counter > 11:
        x=days_total
        y=100*fit2
        line_1, = plot(x,y, color='grey', ls = '--')
        line_1.set_label('FIT Infected')

        x=days_total
        y=100*fit1
        line_1, = plot(x,y, color='grey', ls =  '-.')
        line_1.set_label('FIT Immune')

    # Erstellen der Datenreihen für Liveplot

    x=np.arange(np.nonzero(people_alive)[0][0], np.nonzero(people_alive)[0][-1]+1)
    y=100*people_immune[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1]
    line_1, = plot(x,y, '#B5E51D')
    line_1.set_label('Immune')

    y=100*people_infected[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1]
    line_1, = plot(x,y,'#FEAEC9')
    line_1.set_label('Infected')

    y=100*people_dead[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1]
    line_1, = plot(x,y,'#FE0000')
    line_1.set_label('Deceased')
    legend(loc='upper left')
    plt.title('Live Progression, Day: %i' %day_counter)
    xlabel('Days')
    ylabel('Part of Population [%]')

    # R-Rate auf sekundärer Achse für separate Skalierung
    plt2 = plt.twinx()
    y=r0_current[np.nonzero(people_alive)[0][0]:np.nonzero(people_alive)[0][-1]+1]
    line_1, = plt2.plot(x,y)
    line_1.set_label("$R_0$")
    plt2.legend(loc='upper right')
    plt2.set_ylabel('$R_0$')


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

# === Init Parameter
params = Params()
ini_start() # opens initialise GUI
params = new_parameter()

# === Init pygame ===
pygame.init()
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


def GUI_function():
        button_event = 'none'   # clears variable for next round
        if not gui_queue.empty():  #makes sure that something was sent
            button_event = gui_queue.get() #UI transfers data in form of a string

        if (button_event == 'isolation_up'):
            params.event_isolation_population = params.event_isolation_population + 5

            if params.event_isolation_active:  #takes over new parameter while isolation is active
                for people in population:
                    if not people.heavy and people.alive:
                        people.isolated = False # reset isolation parameter cause otherwise the effect would sum up
                        if (randint(0, 100) <= params.event_isolation_population):
                            people.isolated = True


        elif (button_event == 'isolation_down'):
            event_isolation_population = params.event_isolation_population - 5
            if params.event_isolation_active:
                for people in population:
                    if not people.heavy and people.alive:
                        people.isolated = False
                        if (randint(0, 100) < params.event_isolation_population):
                            people.isolated = True

        elif (button_event == 'isolation_activate'):

            if params.event_isolation_active == False:
                params.event_isolation_active = True
                params.isolation_enabled = True
                for people in population:
                    if (randint(0, 100) < params.event_isolation_population) and people.alive:
                        people.isolated = True
            elif params.event_isolation_active == True:  # Isolation aufgehoben für nicht-schwer Erkrankte
                params.event_isolation_active = False
                params.isolation_enabled = False
                for people in population:
                    if not people.heavy and people.alive:
                        people.isolated = False

        elif (button_event == 'vaccination_up'):
            params.event_vaccination_rate += 5

        elif (button_event == 'vaccination_down'):
            params.event_vaccination_rate -= 5

        elif (button_event == 'vaccination_activate'):
            for people in population:
                if people.alive and not people.sick and not people.infected and (randint(0,100) <= params.event_vaccination_rate):
                    people.immune = True
                    people.image = pygame.image.load("green square 2.jpg")


        elif (button_event == 'cure_rate_up'):
            params.event_cure_rate += 5

        elif (button_event == 'cure_rate_down'):
            params.event_cure_rate -= 5

        elif (button_event == 'cure_activate'):
            for people in population:
                if people.alive and people.sick and (randint(0, 100) <= params.event_cure_rate):
                    people.sick = False
                    people.immune = True
                    people.image = pygame.image.load("green square 2.jpg")


# === PROGRAM ===
if __name__ == "__main__":
    screen = pygame.display.set_mode(size)
    population = []

    #Aufbau GUI
    gui_queue = Queue()  #the communication channel between GUI and main process
    gui_process = Process(target= GUI.gui, args = (gui_queue,))  # starts GUI process
    gui_process.start()

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
    start = timer()
    figure() #erstellt das Figure aus der drawnow-Bibliothek für Liveplot
    # Creating the Simulation
    while sim_continue(population):

        count += 1

        #Abfrage der GUI und auslösen von Events 

        #params.isolation ist während des Programms über die Pfeiltasten rechts und links steuerbar.
        for event in pygame.event.get():

            # check if Pause button is pressed
            clickPauseEvent(event, population)

            if event.type == KEYDOWN and event.key == K_RIGHT:
                for people in population:
                    if randint(0,100)<60:  #Mit einer Wahrscheinlihckeit von 60% halten sich die Personen an die Regeln
                        people.isolated = True
            elif event.type == KEYDOWN and event.key == K_LEFT:
                for people in population:
                    if not people.heavy or people.alive:
                        people.isolated = False
                        params.isolation_enabled = False

         #Impfstoff sofort für alle Kranken verfügbar
            elif (event.type == KEYDOWN and event.key == K_UP):
                for people in population:
                    if people.sick or people.infected:
                        people.sick = False
                        people.infected = False
                        people.immune = True
                        people.image = pygame.image.load("green square 2.jpg")


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
        def process1():  #Erstellen eines Prozesses, um später eine parallele Bearbeitung zu ermöglichen. 
            #start = timer()
            for person in population:
                if 'grids' in globals(): # Grenzen / mehrere Bereiche existieren
                    if person == population[0]:
                        #Grenzlinien zeichnen bei erster Person
                        for i in range(len(grids)):
                            pygame.draw.line(screen, (0,0,0),(0,grids[i]), (width,grids[i]))
                            pygame.draw.line(screen, (0,0,0),(grids[i],0), (grids[i], height))

                    # seperate Betrachtung der Koordinatenrichtungen, Koordinate 1
                    # mit bisect wird überprüft, zwischen welchen Grenzen (in welchem Bereich) sich die Person vor
                    # befindet und nach Bewegung befindet -> Grenzüberschritt bei Veränderung 

                    if (bisect.bisect_left(grids, person.ps.move(person.speed)[0]) != bisect.bisect_left(grids, person.ps[0])) \
                        & (bisect.bisect_left(grids, person.ps.move(person.speed)[0]*-1) == bisect.bisect_left(grids, person.ps[0])):
                        # Person überschreitet Grenze bei Bewegeung, aber nicht bei Bewegung in die Gegenrichtung
                        if randint(0,100) > params.cross_prob:
                            #Grenzübertritt findet nicht statt
                            person.speed[0] = person.speed[0] * -1

                            # Attribut wird auf Penalty-Wert aus Params gesetzt, Vorzeichen orientiert sich an Bewegungsrichtung
                            if person.speed[0] < 0:
                                person.grenzevent_x = -params.grenze_penalty
                            else:
                                person.grenzevent_x = params.grenze_penalty

                    elif (bisect.bisect_left(grids, person.ps.move(person.speed)[0]) != bisect.bisect_left(grids, person.ps[0])) \
                        & (bisect.bisect_left(grids, person.ps.move(person.speed)[0]*-1) != bisect.bisect_left(grids, person.ps[0])):
                        # Person überschreitet Grenze bei Vorwärts- und Rückwärtsbewegung
                        if randint(0,100) > params.cross_prob:
                            if person.speed[0] > 0:
                                person.grenzevent_x = -params.grenze_penalty
                            else:
                                person.grenzevent_x = params.grenze_penalty
                            person.speed[0] = 0

                    # Koordinate 2, genauere Beschreibung in Koordinate 1, Prinzip ist das gleiche 


                    if (bisect.bisect_left(grids, person.ps.move(person.speed)[1]) != bisect.bisect_left(grids, person.ps[1])) \
                        & (bisect.bisect_left(grids, person.ps.move(person.speed)[1]*-1) == bisect.bisect_left(grids, person.ps[1])):
                        # Person überschreitet Grenze bei Bewegeung, aber nicht bei Bewegung in die Gegenrichtung
                        if randint(0,100) > params.cross_prob:
                            person.speed[1] = person.speed[1] * -1
                            if person.speed[1] < 0:
                                person.grenzevent_y = -params.grenze_penalty
                            else:
                                person.grenzevent_y = params.grenze_penalty
                    elif (bisect.bisect_left(grids, person.ps.move(person.speed)[1]) != bisect.bisect_left(grids, person.ps[1])) \
                        & (bisect.bisect_left(grids, person.ps.move(person.speed)[1]*-1) != bisect.bisect_left(grids, person.ps[1])):
                        # Person überschreitet Grenze bei Vorwärts- und Rückwärtsbewegung
                        if randint(0,100) > params.cross_prob:
                            if person.speed[1] > 0:
                                person.grenzevent_y = -params.grenze_penalty
                            else:
                                person.grenzevent_y = params.grenze_penalty
                            person.speed[1] = 0



        def process2():  #Erstellen eines Prozesses, um später eine parallele Bearbeitung zu ermöglichen. 
            for person in population:
                #Die beiden ifs sollen Personen daran hindern, an der Grenze kleben zu bleiben
                if person.grenzevent_x < 0:
                    # versuchter Grenzübertritt innerhalb der letzten Schritte
                    person.speed[0] = randint(-4,0)*params.up #Bewegung von Grenze weg wird erzwungen
                    person.grenzevent_x += 1 #Attribut geht wieder Richtung 0
                elif person.grenzevent_x > 0:
                    # gleiches Prinzip, andere Bewegungsrichtung
                    person.speed[0] = randint(0,4)*params.up
                    person.grenzevent_x -= 1

                # gleiches Prinzip für zweite Koordinatenrichtung
                if person.grenzevent_y < 0:
                    person.speed[1] = randint(-4,0)*params.up
                    person.grenzevent_y += 1
                elif person.grenzevent_y > 0:
                    person.speed[1] = randint(0,4)*params.up
                    person.grenzevent_y -= 1

                person.ps = person.ps.move(person.speed)
                # Abfragen, ob Person Bereich des Bildschirms verlässt
                if person.ps.left < 0 or person.ps.right > width:
                    person.speed[0] = person.speed[0] * -1
                if person.ps.top < 0 or person.ps.bottom > height:
                    person.speed[1] = person.speed[1] * -1

                if count == 0:
                    person.new_step()
                screen.blit(person.image, person.ps)


        def process3(): #Erstellen eines Prozesses, um später eine parallele Bearbeitung zu ermöglichen.
            # Interaktion zwischen zwei Personen
            for person in population:
                for friend in population:
                        if person is friend:
                            pass
                        else:
                            if person.infected or person.sick or person.heavy:
                                    person.contact(friend)


        def process4(count,day_counter): #Erstellen eines Prozesses, um später eine parallele Bearbeitung zu ermöglichen.


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

            people_infected[day_counter]=inf/params.popsize
            if inf_2==0:
                darkfigure[day_counter] = 0
            else:
                darkfigure[day_counter] = (inf+fin)/inf_2
            people_immune[day_counter]=imm/params.popsize
            people_dead[day_counter]=dead/params.popsize
            people_alive[day_counter]=1-dead/params.popsize

            #R0-Berechnung nach RKI: https://www.heise.de/newsticker/meldung/Corona-Pandemie-Die-Mathematik-hinter-den-Reproduktionszahlen-R-4712676.html
            if day_counter > 7:
                r0 = (people_infected[day_counter] + people_infected[day_counter-1] + people_infected[day_counter-2] + people_infected[day_counter-3] ) / ( people_infected[day_counter-4] + people_infected[day_counter-5] +people_infected[day_counter-6]+people_infected[day_counter-7])
                r0_current[day_counter] = r0
            if day_counter == 0:
                r0_current[0] = 1
            if day_counter==1:
                r0 = people_infected[1] / people_infected[0]
                r0_current[1] = r0

            if day_counter==2:
                r0 = people_infected[2] / people_infected[1]
                r0_current[2] = r0

            if day_counter>=3 and day_counter <=7:
                r0 = (people_infected[day_counter]+people_infected[day_counter-1]) / (people_infected[day_counter-2] + people_infected[day_counter-3])
                r0_current[day_counter] = r0


            # Ausgabe des Status über Konsole
            print("Tag: ",day_counter,".....","Isolationsaufruf: ",params.isolation_enabled,".....","r0: ", \
                  round(r0_current[day_counter],4),".....","aktuell Infizierte: ", round(people_infected[day_counter],4), \
                  ".....","Dunkelziffer: ",round(darkfigure[day_counter],3),".....","aktuell Immune: ", \
                  round(people_immune[day_counter],4),".....","aktuell Verstorbene: ",round(people_dead[day_counter],4))



        process3 = multiprocessing.Process(target=process3())#Ausführen des Prozesses mittels Multiprocessing
        GUI_function()
        if count==12:
            end = timer()#Timer enden
            print("Laufzeit",end-start)#Wert des Timers ausgeben
            start = timer()# Timer starten
            day_counter += 1
            process4 = multiprocessing.Process(target=process4(count,day_counter))#Ausführen des Prozesses mittels Multiprocessing
            if day_counter > 9 and day_counter % 6 == 0:
                fit1,fit2,days_total = fitting(params.infected/params.popsize, max_days,day_counter,people_immune,people_infected)#Alle 6 Tage wird Fitting aufgerufen und eine neue Vorhersage wird erstellt.
            drawnow(drawfkt)
            count = 0

        process1 = multiprocessing.Process(target=process1())#Ausführen des Prozesses mittels Multiprocessing
        process2 = multiprocessing.Process(target=process2())#Ausführen des Prozesses mittels Multiprocessing

        pygame.display.flip()


# === AUSWERTUNG ===
    if params.result == True:
        # Aufruf der einzelnen Funktionen zur Auswertung
        statistics(population,params,day_counter)
        Auswertung_Excel = True
        if Auswertung_Excel:
            Excel_Auswertung (r0_current,people_infected, darkfigure, people_immune, people_dead)

        Plot_interaktiv(people_alive, people_immune, people_infected, people_dead, r0_current)

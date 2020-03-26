"""
Program: Coronavirus Simulation
Author: Nathan Verghis
Date: March 18, 2020
I created this program in light of the coronavirus epidemic. I was inspired by
the vast confusion people had surrounding the need for isolation. I felt that by
creating this program, it could better teach people about why isolation is so
important in preventing the spread of a virus. Plans on expanding in the future
could involve creating a special member of the People class (compromised person)
to show the effectiveness of herd immunity on protecting a member of the
population who can't be relied on recovering from a disease on their own. I can
also expand the program to collect data from different iterations at different
values of infected and isolation to then graph in Matlab to better depict the
effect of isolation.
"""

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
scale = 800 #Skalierung
up = 1.2   #Bewegungsgeschwindigkeit der Personen

popsize = scale


end_dist = pd.DataFrame(columns=['Age','Alive'],index=range(popsize))

dev_mode = True
result = True

if dev_mode == True:

    isolation = 0#100
    infected = 2
    infection_chance = 60#100
    recovery = 8
    heavy_case = 5#2
    incubation_time = 6
    superspreader = 10

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
mort_rate = [[0,(0+0.2)/2],[20,0.2],[40,(0.4+1.3)/2],[60,(3.6+8)/2],[80,14.8]]
#Sterblichkeitsrate über Alter nach (https://www.dw.com/de/coronavirus-endlich-umfassende-daten-aus-china/a-52421582)
#Quelle: Chinese Center for Disease Control and Prevention
#erster Eintrag: Untergrenze Alter, zweiter Eintrag: Sterblichkeitsrate angepasst an Altersverteilung

# === DEF ===

# Creating People object
class Person:
    """A single person in the game. Has attributes of being sick, isolated, and
    alive. Meant to interact with another member of its population to create
    the simulation."""
    def __init__(self, isolated, sick,immune,heavy,infected,superspread):
        self.alive = True
        self.immune = False
        self.isolated = isolated
        self.infected = infected
        self.sick = sick
        self.heavy = heavy
        self.age = 0
        self.mortality = 0
        self.dead =False
        self.superspread = superspread
        if self.isolated:
            self.speed = [0, 0]

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
        self.left = randint(1, scale/(10))
        self.top = randint(1, scale/(10))
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

    def new_day(self):
        """The change from day to day for a sick person.
        They can either recover or die
        If dead then they have no more impact on the population"""
        #if input() == i:
        #    self.isolated = True

        if self.isolated:
            self.speed = [0, 0]
        if self.superspread:
            pass
        elif not self.alive == 0:
            self.speed = [randint(-100, 100) * 0.04*up, randint(-100, 100) * 0.04*up]

        if self.infected:
            if randint(1,100) < incubation_time:
                self.infected = False
                self.sick = True
                self.alive = True

                self.image = pygame.image.load("red box 2.jpg")

        if self.sick:

            if randint(1, 100) < heavy_case:
                self.isolated = True
                self.superspread = False
                self.speed = [0, 0]
                self.alive = True
                self.heavy = True
                self.sick = True
                self.image = pygame.image.load("red box 2.jpg")
            elif randint(1, 100) < recovery:
                self.sick = False
                self.immune = True
                self.alive = True
                self.speed = [randint(-100, 100) * 0.05, randint(-100, 100) * 0.05]
                self.image = pygame.image.load("green square 2.jpg")

        if self.heavy:

            if randint(1, 100) < self.mortality:
                self.isolated = True
                self.superspread = False
                self.speed = [0, 0]
                self.alive = False
                self.heavy = False
                self.immune = False
                self.dead = True
                self.sick = False
                #self.immune = False
                self.image = pygame.image.load("dark red 2.jpg")
            elif randint(1, 100) < recovery:
                self.sick = False
                self.immune = True
                self.alive = True
                self.speed = [randint(-100, 100) * 0.05, randint(-100, 100) * 0.05]
                self.image = pygame.image.load("green square 2.jpg")


    def contact(self, other):
        """The event that two people come in contact with each other.
        Handles the case where the infection spreads
        Also handles the change in direction as they part ways
        Isolated people dont come into contact so people pass through them"""
        if self.ps.colliderect(other.ps) and not self.immune and not other.immune and not self.isolated and not other.isolated:
            self.speed[0], self.speed[1] = \
                self.speed[0] * -1, self.speed[1] * -1
            other.speed[0], other.speed[1] = \
                other.speed[0] * -1, other.speed[1] * -1
            if self.sick and not other.sick:
                if infection_chance > randint(0,100):
                    other.infected = True
                    other.image = pygame.image.load("rosa box.jpg")
            elif not self.sick and other.sick:
                if infection_chance >  randint(0,100):
                    self.infected = True
                    self.image = pygame.image.load("rosa box.jpg")

            if self.infected and not other.sick:
                if infection_chance > randint(0,100):
                    other.infected = True
                    other.image = pygame.image.load("rosa box.jpg")
            elif not self.sick and other.infected:
                if infection_chance >  randint(0,100):
                    self.infected = True
                    self.image = pygame.image.load("rosa box.jpg")
        if self.ps.colliderect(other.ps) and not self.immune and not other.immune: # and not self.isolated and not other.isolated:
            self.speed[0], self.speed[1] = \
                self.speed[0] * -1, self.speed[1] * -1
            other.speed[0], other.speed[1] = \
                other.speed[0] * -1, other.speed[1] * -1
            if self.sick and not other.sick:
                if infection_chance/2 > randint(0,100):
                    other.infected = True
                    other.image = pygame.image.load("rosa box.jpg")
            elif not self.sick and other.sick:
                if infection_chance/2 >  randint(0,100):
                    self.infected = True
                    self.image = pygame.image.load("rosa box.jpg")

            if self.infected and not other.sick:
                if infection_chance/2 > randint(0,100):
                    other.infected = True
                    other.image = pygame.image.load("rosa box.jpg")
            elif not self.sick and other.infected:
                if infection_chance/2 >  randint(0,100):
                    self.infected = True
                    self.image = pygame.image.load("rosa box.jpg")


def sim_continue(pop):
    """Tells the simulation if there is any point in continuing.
    End of simulation defined as the event when the whole population is either
    dead or completely recovered."""
    all_dead = all(not people.alive for people in pop)
    all_healed = all(not people.sick and not people.infected for people in pop)
    return not(all_dead or all_healed)


def statistics(pop):
    """Informs the user of population statistics following the extermination of
    either the population or the virus"""
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

# Creating the population
for i in range(popsize):
    is_isolated = False
    is_infected = False
    is_immune = False
    is_heavy = False
    is_superspread = False
    temp = randint(1, popsize)
    if temp < isolation:
        is_isolated = True
    if temp < infected:
        is_infected = True
    if temp < superspreader:
        is_superspread = True
    new_person = Person(is_isolated, is_infected,is_immune,is_heavy,is_infected,is_superspread)
    end_dist['Age'][i] = new_person.age
    new_person.ps = new_person.ps.move(new_person.left*10, new_person.top*10)
    population.append(new_person)
days = np.ones(100)
days[0] = 0
people_infected = np.zeros(1000)
people_immune = np.zeros(1000)
people_dead = np.zeros(1000)
people_alive = np.zeros(1000)
people_infected[0] = infected/popsize
# Creating the Simulation
while sim_continue(population):
    count += 1
    if count == 8:
        day_counter += 1


    inf=0
    imm=0
    dead=0
    for people in population:
        if people.infected ==True:
            inf+=1
        if people.sick == True:
            inf+=1
        if people.immune ==True:
            imm +=1
        if people.dead == True:
            dead +=1
    people_infected[day_counter]=inf/popsize
    people_immune[day_counter]=imm/popsize
    people_dead[day_counter]=dead/popsize
    people_alive[day_counter]=1-dead/popsize
    if count == 8:
        print(day_counter,".....",people_infected[day_counter],".....",people_immune[day_counter],".....",people_dead[day_counter],".....",100*people_infected[day_counter]/people_infected[day_counter-1]-100)
        count = 0
    #time.sleep(0.001)
    #Exit Key (right arrow)
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_RIGHT:
            sys.exit()

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
            person.new_day()
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

    # Achsen-Bereiche manuell festlegen
    # Syntax: plt.axis([xmin, xmax, ymin, ymax])
    #plt.axis([0, 5, 0, 20])

    # Ein gepunktetes Diagramm-Gitter einblenden:
    plt.grid(True)

    # Diagramm anzeigen:
    plt.show()


    """plt.figure(figsize=(12,6))
    plt.style.use('seaborn-darkgrid')
    end_dist['Age'].value_counts().sort_index().plot(c='purple',marker='o',label='Population',markersize=10)
    end_dist[end_dist['Alive']==1]['Age'].value_counts().sort_index().plot(c='blue',marker='o',label='Alive')
    end_dist[end_dist['Alive']==0]['Age'].value_counts().sort_index().plot(c='red',marker='o',label='Deceased')
    plt.legend()
    plt.xlabel('Age')
    plt.ylabel('Count')
    plt.title('Result')
    plt.show()"""

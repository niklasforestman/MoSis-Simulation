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



def statistics(pop,params,day_counter):
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

    print("Days til completion: ", day_counter)
    print("Alive: ", alive)
    print("Dead: ", dead)
    print("Immune: ",immune)


    #return alive, dead, immune, params.end_dist

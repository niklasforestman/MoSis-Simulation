import sys
import pygame
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pygame.locals import *
from random import randint
import time
import numpy as np
import time



def clickPauseEvent(event):
    # is activated via the 'P' for PAUSE key
    #    later versions might include a nice big shiny button insode the GUI
    if event.type == KEYDOWN and event.key == K_p:
        print("++++++++++++++++++++++++++++++")
        print( "EngageGodMode")
        print("++++++++++++++++++++++++++++++")
        godMode()


def godMode():
    #stop the game to run some crazy stuff only a god could possibly do
    #here has to be a while loop with all ralevant steps inside th godMode
    print("++++++++++++++++++++++++++++++")
    print("I AM GOD!")
    print("++++++++++++++++++++++++++++++")
    statusGodmode = True
    while statusGodmode:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_z:
                statusGodmode = False
                print("You have no power here!")
                print("GodMode removed")

    #while True:
        #do the relevant stuff

        #

       # if #resume playing is activated
           # break

def wululululu(x, y):
    for people in population:
        if True:
            pass
    pass

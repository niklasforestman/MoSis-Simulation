import pygame
from pygame.locals import *




def clickPauseEvent(event, population):
    # is activated via the 'P' for PAUSE key
    #    later versions might include a nice big shiny button insode the GUI
    if event.type == KEYDOWN and event.key == K_p:
        print("++++++++++++++++++++++++++++++")
        print( "EngageGodMode")
        print("++++++++++++++++++++++++++++++")
        godMode(population)


def godMode(population):
    #stop the game to run some crazy stuff only a god could possibly do
    #here has to be a while loop with all ralevant steps inside th godMode
    print("++++++++++++++++++++++++++++++")
    print("I ... AM ... A ... GOD!")
    print("++++++++++++++++++++++++++++++")
    statusGodmode = True
    while statusGodmode:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_z:
                statusGodmode = False
                print("++++++++++++++++++++++++++++++")
                print(" You are no power here!")
                print(" -> or are no longer worhty enough")
                print(" -> or killed someone innocent")
                print("")
                print(" GodMode removed ")
                print("++++++++++++++++++++++++++++++")

            if event.type == MOUSEBUTTONDOWN :
                print(event.pos) #Gibt die Position relaitv zur oberen linken Ecke des Fensters aus
                wululululu(event.pos, population)



def wululululu(pos, population):
    print("X = ", pos[0])
    print("y = ", pos[1])
    aoe = 2
    durchzählen = 1
    #for person in population:
    #    durchzählen += 1
    #    if abs(person.ps[0] - pos[0]) <= aoe and abs(person.ps[1] - pos[1]) <= aoe:
    #        print(durchzählen)
    #        print("Du sollst vom Blitz getroffen werden")
    durchzaehlen = 1
    for person in population:
        durchzaehlen += 1
        if abs(person.ps[0] - pos[0]) <= aoe and abs(person.ps[1] - pos[1]) <= aoe:
            print(durchzaehlen)
            print("SPÜRE MEINE MACHT !!!")
            print(person.ps)


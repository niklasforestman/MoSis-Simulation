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
                print(" Godlike permissions removed ")
                print("++++++++++++++++++++++++++++++")

            if event.type == MOUSEBUTTONDOWN :
                print(event.pos) #Gibt die Position relaitv zur oberen linken Ecke des Fensters aus
                wululululu(event.pos, population)

def anleitungAuswahl():
    print("Very well. Wich parameter would you like to change ?")
    print("++++++++++++++++++++++++++++++")
    print("press [a] for alive")
    print("press [s] for sick")
    print("press [i] for infected")
    print("press [o] for isolated")
    print("press [h] for heavy")
    print("press [d] for dead")
    print("press [p] for superspread")
    print("press [m] for immune")
    print("")
    print("press [esc] to pick another person")
    print("press [esc] first and then press [z] to resume the simulation")
    print("++++++++++++++++++++++++++++++")


def pickAStatusAlready(person):

    #Attribute einer Prson: ['alive','immune', 'isolated', 'infected', 'sick', 'heavy', 'dead', 'superspread']

    print("++++++++++++++++++++++++++++++")
    print("AHHHHH I SEE YOU WANNE BE A GOD")
    print("")
    anleitungAuswahl()

    myBreakCondition = True

    while myBreakCondition:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    person.alive = not person.alive
                    print("you pressed [a] for ALIVE")
                    print("persons status alive changed from: ", not person.alive)
                    print("persons status alive is now", person.alive)
                    anleitungAuswahl()

                elif event.key == pygame.K_s:
                    person.sick = not person.sick
                    print("you pressed [s] for SICK")
                    print("persons status alive changed from: ", not person.sick)
                    print("persons status alive is now", person.sick)
                    anleitungAuswahl()

                elif event.key == pygame.K_i:
                    person.alive = not person.infected
                    print("you pressed [i] for infected")
                    print("persons status alive changed from: ", not person.infected)
                    print("persons status alive is now", person.infected)
                    anleitungAuswahl()

                elif event.key == pygame.K_o:
                    person.alive = not person.isolated
                    print("you pressed [o] for isolated")
                    print("persons status alive changed from: ", not person.isolated)
                    print("persons status alive is now", person.isolated)
                    anleitungAuswahl()

                elif event.key == pygame.K_h:
                    person.alive = not person.heavy
                    print("you pressed [h] for heavy")
                    print("persons status alive changed from: ", not person.heavy)
                    print("persons status alive is now", person.heavy)
                    anleitungAuswahl()

                elif event.key == pygame.K_d:
                    person.alive = not person.dead
                    print("you pressed [d] for dead")
                    print("persons status alive changed from: ", not person.dead)
                    print("persons status alive is now", person.dead)
                    anleitungAuswahl()

                elif event.key == pygame.K_p:
                    person.alive = not person.superspread
                    print("you pressed [p] for superspread")
                    print("persons status alive changed from: ", not person.superspread)
                    print("persons status alive is now", person.superspread)
                    anleitungAuswahl()

                elif event.key == pygame.K_m:
                    person.alive = not person.immune
                    print("you pressed [m] for immune")
                    print("persons status alive changed from: ", not person.immune)
                    print("persons status alive is now", person.immune)
                    anleitungAuswahl()

                elif event.key == pygame.K_ESCAPE:
                    print("escape pressed")
                    print(" okay done with this Person !?")
                    print(" pick another or resume simulation with [z]")
                    myBreakCondition = False


def wululululu(pos, population):
    print("X = ", pos[0])
    print("y = ", pos[1])
    aoe = 2

    pearsonHit = False
    durchzaehlen = 1

    for person in population:
        durchzaehlen += 1
        if abs(person.ps[0] - pos[0]) <= aoe and abs(person.ps[1] - pos[1]) <= aoe:
            pearsonHit = True

            pickAStatusAlready(person)

            print(durchzaehlen)
            print(person.ps)
            print("SPÜRE MEINE MACHT !!!")

    if pearsonHit == False:
        print("...you missed...")
        print("...even a God can't be angry at the big white nothingness...")


    print("++++++++++++++++++++++++++++++")

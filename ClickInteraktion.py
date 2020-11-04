import pygame
from pygame.locals import *

# Thins document is to enable the clickinteraction with single indivuduals of the Population.
#       if you press "p" you pause the simulation nd enter into the GODMODE where you canindividually
#       alter the atributes of individual people ou selected.
#       An individual can be selected by clicking on it. That will give you back an instrcution
#       in the console on how to alter a persons atributes.


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
            if event.type == KEYDOWN and event.key == K_z:  #   if z is pressed  you can exit the GODMODE and get an according message
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

def anleitungAuswahl(person):   # This is the function that prints instructions in the console on how to alter
                                #       a persons attributes
    print("Very well. Wich parameter would you like to change ?")
    print("++++++++++++++++++++++++++++++")
    print("press [a] for alive.         The alive statuts is currenly", person.alive)
    print("press [s] for sick.          The sick statuts is currenly",person.sick )
    print("press [i] for infected.      The infected statuts is currenly",person.infected)
    print("press [o] for isolated.      The isolated statuts is currenly",person.isolated)
    print("press [h] for heavy.         The heavy statuts is currenly",person.heavy)
    print("press [d] for dead.          The dead statuts is currenly",person.dead)
    print("press [p] for superspread.   The superspread statuts is currenly",person.superspread)
    print("press [m] for immune.        The immune statuts is currenly",person.immune)
    print("")
    print("press [esc] to pick another person")
    print("press [esc] first and then press [z] to resume the simulation")
    print("++++++++++++++++++++++++++++++")


def pickAStatusAlready(person):     # This function is the functionality that enables someone in
                                    #       GODMODE to change an individuals attributes inside the simulation

    #Attribute einer Prson: ['alive','immune', 'isolated', 'infected', 'sick', 'heavy', 'dead', 'superspread']

    print("++++++++++++++++++++++++++++++")
    print("AHHHHH I SEE YOU WANNE BE A GOD")
    print("")
    anleitungAuswahl(person)        # Prints the instrucitons inside the console

    myBreakCondition = True

    while myBreakCondition:

        for event in pygame.event.get():    #   loop that checks all the different possibilitys
                                            #       the attributes can changed with keypresses
                                            #       according to the instructions printed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    person.alive = not person.alive
                    print("you pressed [a] for ALIVE")
                    print("persons status alive changed from: ", not person.alive)
                    print("persons status alive is now", person.alive)
                    anleitungAuswahl(person)

                elif event.key == pygame.K_s:
                    person.sick = not person.sick
                    print("you pressed [s] for SICK")
                    print("persons status SICK changed from: ", not person.sick)
                    print("persons status SICK is now", person.sick)
                    anleitungAuswahl(person)

                elif event.key == pygame.K_i:
                    person.alive = not person.infected
                    print("you pressed [i] for INFECTED")
                    print("persons status INFECTED changed from: ", not person.infected)
                    print("persons status INFECTED is now", person.infected)
                    anleitungAuswahl(person)

                elif event.key == pygame.K_o:
                    person.alive = not person.isolated
                    print("you pressed [o] for ISOLATED")
                    print("persons status ISOLATED changed from: ", not person.isolated)
                    print("persons status ISOLATED is now", person.isolated)
                    anleitungAuswahl(person)

                elif event.key == pygame.K_h:
                    person.alive = not person.heavy
                    print("you pressed [h] for HEAVY")
                    print("persons status HEAVY changed from: ", not person.heavy)
                    print("persons status HEAVY is now", person.heavy)
                    anleitungAuswahl(person)

                elif event.key == pygame.K_d:
                    person.alive = not person.dead
                    print("you pressed [d] for DEAD")
                    print("persons status DEAD changed from: ", not person.dead)
                    print("persons status DEAD is now", person.dead)
                    anleitungAuswahl(person)

                elif event.key == pygame.K_p:
                    person.alive = not person.superspread
                    print("you pressed [p] for SUPERSPREAD")
                    print("persons status SUPERSPREAD changed from: ", not person.superspread)
                    print("persons status SUPERSPREAD is now", person.superspread)
                    anleitungAuswahl(person)

                elif event.key == pygame.K_m:
                    person.alive = not person.immune
                    print("you pressed [m] for IMMUNE")
                    print("persons status IMMUNE changed from: ", not person.immune)
                    print("persons status IMMUNE is now", person.immune)
                    anleitungAuswahl(person)

                elif event.key == pygame.K_ESCAPE:
                    print("escape pressed")
                    print(" okay done with this Person !?")
                    print(" pick another or resume simulation with [z]")
                    myBreakCondition = False


def wululululu(pos, population):    # This function allows that a person from the population can
                                    #       be selected via a mouse click.
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

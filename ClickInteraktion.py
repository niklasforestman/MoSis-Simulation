import pygame
from pygame.locals import *     # import pacages needed to use user input funtionality of pygame
import ClickInteractionGUI      # import the GUI so we are able to call the GUI from here


def clickPauseEvent(event, population):
    # is activated via the 'P' for PAUSE key. The call for this function happens in the main "simulation" loop
    # This function only checks if the key "p" is pressed on the keyboard.
    # This function gets the current population (list of people) and the pygame event os arguments.

    if event.type == KEYDOWN and event.key == K_p:  # does something f the key "p" on the keyboard is pressed

        print("++++++++++++++++++++++++++++++")
        print( "EngageGodMode")
        print("++++++++++++++++++++++++++++++")     # printing out some information in the console... funny and usefull
                                                    # for finding errors

        godMode(population)     # calls the "Godmode" functionality if the "p" key on the keyboard is pressed
                                # The population (list of pearsons) that was given to the clickPauseEvent function is
                                # is given to the godMode function as an argument, so the Godmode function can manipulate
                                # the population of all people


def godMode(population):
    # Gets called if the "p" key is pressed.
    # Stops the game to run some crazy stuff only a god could possibly do.
    # Defines the "Godmode" functionality.
    # gets the population as an argument so every person in the population can be manipulated

    print("++++++++++++++++++++++++++++++")
    print("I ... AM ... A ... GOD!")
    print("++++++++++++++++++++++++++++++")     # printing out some information in the console... funny and usefull
                                                # for finding errors

    statusGodmode = True    # sets the godmode Variable to True. This is needed to keep the following while-loop
                            # running until the break condition is met.


    while statusGodmode:        # This while-loop runs continously once the "p" key is pressed. This loop keeps on running for
                                # ever and ever and ever and ever... until you meet the break criteria

        for event in pygame.event.get():        # this is one of the functionalitys of pygame.  It outs all the user
                                                # inputs into a queue and iterates over the queue. So if you press something
                                                # that interaction gets put into the queue.

            if event.type == KEYDOWN and event.key == K_z:      # if the element in the queue is the "z" key on the keyboard
                                                                # the following commands are executed.

                statusGodmode = False       # the godmode Variable is set to false. Therefore the while-loop will be broken
                                            # therefore prssing the "z" key is the break condition for the Godmode

                print("++++++++++++++++++++++++++++++")
                print(" You are no power here!")
                print(" -> or are no longer worhty enough")
                print(" -> or killed someone innocent")
                print("")
                print(" Godlike permissions removed ")
                print("++++++++++++++++++++++++++++++")     # printing out some information in the console... funny and usefull
                                                            # for finding errors

            if event.type == MOUSEBUTTONDOWN :      # if the element in the queue is a mouseclick the commands
                                                    # inside this if-loop will be executed

                print(event.pos)        #returns the position of the mouse at the moment the mouse was clicked

                wululululu(event.pos, population)       # This calls the wululululu function. (see the definition of wululululu)
                                                        # The wululululu function gets the event.pos as arguments. This
                                                        # is the position of the mouseclick in the simulation window.
                                                        # it also recieves the population (list of all persons) as an
                                                        # argument so they can be influenced.

'''

def anleitungAuswahl(person):   # THIS FUNCTION IS NOT IN USE.
    # This function is a manuel on how to influence the person given to the function person.

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
    print("++++++++++++++++++++++++++++++")     # printing out some information in the console... funny and usefull
                                                # for finding errors
                                                
'''

'''
def pickAStatusAlready(person):     # THIS FUNCTION IS NOT IN USE.
    # This function implements the basic functionality to alter the various attributes of a person vie the terminal.
    # This function only uses keyboard presses and the anleitungAuswahl function as a guide to influence the attributes
    # of a person.

    #Attribute einer Prson: ['alive','immune', 'isolated', 'infected', 'sick', 'heavy', 'dead', 'superspread']

    print("++++++++++++++++++++++++++++++")
    print("AHHHHH I SEE YOU WANNE BE A GOD")
    print("")   # printing out some information in the console... funny and usefull
                # for finding errors


    anleitungAuswahl(person)    # calls the anleitungAuswahl funciton to give the user the information on how to
                                # influence a persons attribute

    myBreakCondition = True     # sets a breakflag to true, so the following while-loop will continue to loop untill the
                                # break condition is met

    while myBreakCondition:     # While loop to wait for user input once the function pickAStatusAlready is called

        for event in pygame.event.get():        # the already known for-loop from pygame that puts all user inputs into a
                                                # list and then iterates over the list of user inputs.

            if event.type == pygame.KEYDOWN:    # checks if the event is a pressed key (in contrast to a mouse click or something)


                #the following if-conditions check for the different pressed keys

                if event.key == pygame.K_a:                      # key "a"
                    person.alive = not person.alive              # inverts the current status of the person
                    print("you pressed [a] for ALIVE")           # prints information about the chosen attribute
                    print("persons status alive changed from: ", not person.alive)
                    print("persons status alive is now", person.alive)
                    anleitungAuswahl(person)                      # prints the manual about changing attributes again

                elif event.key == pygame.K_s:       # analogous to the first case
                    person.sick = not person.sick
                    print("you pressed [s] for SICK")
                    print("persons status SICK changed from: ", not person.sick)
                    print("persons status SICK is now", person.sick)
                    anleitungAuswahl(person)

                elif event.key == pygame.K_i:       # analogous to the first case
                    person.alive = not person.infected
                    print("you pressed [i] for INFECTED")
                    print("persons status INFECTED changed from: ", not person.infected)
                    print("persons status INFECTED is now", person.infected)
                    anleitungAuswahl(person)

                elif event.key == pygame.K_o:       # analogous to the first case
                    person.alive = not person.isolated
                    print("you pressed [o] for ISOLATED")
                    print("persons status ISOLATED changed from: ", not person.isolated)
                    print("persons status ISOLATED is now", person.isolated)
                    anleitungAuswahl(person)

                elif event.key == pygame.K_h:       # analogous to the first case
                    person.alive = not person.heavy
                    print("you pressed [h] for HEAVY")
                    print("persons status HEAVY changed from: ", not person.heavy)
                    print("persons status HEAVY is now", person.heavy)
                    anleitungAuswahl(person)

                elif event.key == pygame.K_d:       # analogous to the first case
                    person.alive = not person.dead
                    print("you pressed [d] for DEAD")
                    print("persons status DEAD changed from: ", not person.dead)
                    print("persons status DEAD is now", person.dead)
                    anleitungAuswahl(person)

                elif event.key == pygame.K_p:       # analogous to the first case
                    person.alive = not person.superspread
                    print("you pressed [p] for SUPERSPREAD")
                    print("persons status SUPERSPREAD changed from: ", not person.superspread)
                    print("persons status SUPERSPREAD is now", person.superspread)
                    anleitungAuswahl(person)

                elif event.key == pygame.K_m:       # analogous to the first case
                    person.alive = not person.immune
                    print("you pressed [m] for IMMUNE")
                    print("persons status IMMUNE changed from: ", not person.immune)
                    print("persons status IMMUNE is now", person.immune)
                    anleitungAuswahl(person)

                elif event.key == pygame.K_ESCAPE:      # this is the break condition from this while-loop
                    print("escape pressed")
                    print(" okay done with this Person !?")
                    print(" pick another or resume simulation with [z]")
                    myBreakCondition = False        # break condition is triggert if escape key is pressed

'''
def wululululu(pos, population):
    # This function has the purpose to modify the attributes of a certain person.
    # gets the position of the mouseclick and the population (list of all persons in the simulation) as arguments

    print("X = ", pos[0])
    print("y = ", pos[1])       # prints the position of the mouseclick in the console
    aoe = 2

    pearsonHit = False
    durchzaehlen = 1

    for person in population:   # for-loop that iterates over every person the population.

        durchzaehlen += 1       # a simple counter variable

        if abs(person.ps[0] - pos[0]) <= aoe and abs(person.ps[1] - pos[1]) <= aoe:
            # this if-loop checks if the position of the current person is reasonably close to the position of the
            # mouseclick that was given as arguments to this function. If the mousclick was close to a person
            # everything inside this if-loop is executed

            pearsonHit = True

            #pickAStatusAlready(person) # OLD VERSION . ONLY ALLOWS MANIPULATION VIA THE TERMINAL
            #--------------------------------------------------------------------------------------

            ClickInteractionGUI.guiErstellen(person)    # this function was imported at the top and is called.
                                                        # It creates a little GUI that allows a graphic manipulation
                                                        # of a persons attribute.
                                                        # for a more in depth description got to click interactionGUI and
                                                        # read the comments.

            #--------------------------------------------------------------------------------------

            print(durchzaehlen)
            print(person.ps)
            print("SPÜRE MEINE MACHT !!!")      # Prints a whole lot of information

    if pearsonHit == False:
        # This if-loop is executed if the mouseclick was not close enough to any of the persons from the population

        print("...you missed...")
        print("...even a God can't be angry at the big white nothingness...")


    print("++++++++++++++++++++++++++++++")
import pygame
from pygame.locals import *

pygame.init()

location = 0
myBreakCondition = True

while myBreakCondition:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                location -= 1
                print(location)
            if event.key == pygame.K_RIGHT:
                location += 1
                print(location)
            if event.key == pygame.K_ESCAPE:
                print("escape pressed")
                myBreakCondition = False

print("fertig")
import sys
import pygame
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pygame.locals import *
from random import randint
import time
import numpy as np
import xlsxwriter

def Excel_Auswertung (r0_current,people_infected, darkfigure, people_immune, people_dead):

    workbook = xlsxwriter.Workbook('Daten_Vergleich.xlsx')
    worksheet = workbook.add_worksheet()
    row = 1
    col = 0

    worksheet.write(0,col,'Tag')
    worksheet.write(0,col+1,'r0')
    worksheet.write(0,col+2,'Aktuell Infizierte')
    worksheet.write(0,col+3,'Dunkelziffer')
    worksheet.write(0,col+4,'Aktuell Immune')
    worksheet.write(0,col+5,'Aktuell Verstorbene')



    for r0 in (r0_current):
        worksheet.write(row, col+1, r0)
        row+=1
    row=1

    for Aktuell_Infizierte in (people_infected):
        worksheet.write(row, col+2, Aktuell_Infizierte)
        row +=1
    row=1
    for Dunkelziffer in (darkfigure):
        worksheet.write(row, col+3, Dunkelziffer)
        row +=1
    row=1
    for Aktuell_Immune in (people_immune):
        worksheet.write(row, col+4, Aktuell_Immune)
        row +=1
    row=1
    for Aktuell_Verstorbene in (people_dead):
        worksheet.write(row, col+5, Aktuell_Verstorbene)
        row +=1
    row=1
    workbook.close()

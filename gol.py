import pygame, led, sys, os, random, csv
import numpy
from pygame.locals import *
from led.PixelEventHandler import *
# from bmpfont import bmpfont

""" A flappy bird clone
"""

random.seed()

BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
IWHITE = 16777215
IRED = 16711680
IGREEN = 65280
IBLUE = 255
IBLACK = 0

# wing1font = bmpfont.BmpFont("bmpfont/wing1-5x5px-white.idx")

# detect if a serial/USB port is given as argument
hasSerialPortParameter = ( sys.argv.__len__() > 1 )

# use 90 x 20 matrix when no usb port for real display provided
fallbackSize = ( 90, 20 )

if hasSerialPortParameter:
    serialport = sys.argv[ 1 ]
    print "INITIALIZING WITH USB-PORT: "+serialport
    ledDisplay = led.dsclient.DisplayServerClientDisplay(serialport, 8123)
else:
    print "INITIALIZING WITH SIMULATOR ONLY."
    ledDisplay = led.dsclient.DisplayServerClientDisplay("localhost", 8123)

# use same size for sim and real LED panel
size = ledDisplay.size()
simDisplay = led.sim.SimDisplay(size)
screen = pygame.Surface(size)
gamestate = 1 #1=alive; 0=dead

Cells = numpy.zeros((90, 20), dtype=numpy.int32)
CellsNew = numpy.zeros((90, 20), dtype=numpy.int32)
# Cells[10,10] = IWHITE

pattern = 0
randomPattern = False

def CountLifeNeighbours(x, y):
    global Cells
    lifeCells = 0
    try:
        if Cells[x-1][y-1] == IWHITE:
            lifeCells += 1
    except:
        pass
    try:
        if Cells[x][y-1] == IWHITE:
            lifeCells += 1
    except:
        pass
    try:
        if Cells[x+1][y-1] == IWHITE:
            lifeCells += 1
    except:
        pass
    try:
        if Cells[x-1][y] == IWHITE:
            lifeCells += 1
    except:
        pass
    try:
        if Cells[x+1][y] == IWHITE:
            lifeCells += 1
    except:
        pass
    try:
        if Cells[x-1][y+1] == IWHITE:
            lifeCells += 1
    except:
        pass
    try:
        if Cells[x][y+1] == IWHITE:
            lifeCells += 1
    except:
        pass
    try:
        if Cells[x+1][y+1] == IWHITE:
            lifeCells += 1
    except:
        pass
    return lifeCells

def isAlive(x, y):
    if Cells[x][y] == IWHITE:
        return True
    else:
        return False

def CheckCells():
    global Cells
    global CellsNew
    for x in range(90):
        for y in range(20):
            CellsNew[x][y] = IBLACK
            life = CountLifeNeighbours(x, y)
            if not isAlive(x, y):
                if life == 3:
                    CellsNew[x][y] = IWHITE
            else:
                if life == 2 or life == 3:
                    CellsNew[x][y] = IWHITE
            # if x < 5 and y < 5:
            #     print x, y, life, isAlive(x, y), Cells[x][y], CellsNew[x][y]

    Cells[:] = CellsNew

def resetGame():
    global Cells
    global pattern
    global randomPattern
    if pattern == 0:
        for x in range(90):
            for y in range(20):
                if random.randint(1,10) > 5:
                    Cells[x][y] = IBLACK
                else:
                    Cells[x][y] = IWHITE
        randomPattern = True
    else:
        for x in range(90):
            for y in range(20):
                Cells[x][y] = IBLACK
        randomPattern = False
        
    if pattern == 1:
        Cells[1][0] = IWHITE
        Cells[2][1] = IWHITE
        Cells[0][2] = IWHITE
        Cells[1][2] = IWHITE
        Cells[2][2] = IWHITE
    elif pattern == 2:
        Cells[0][10] = IWHITE
        Cells[1][10] = IWHITE
        Cells[2][10] = IWHITE

        Cells[5][9] = IWHITE
        Cells[5][10] = IWHITE
        Cells[7][10] = IWHITE
        Cells[4][11] = IWHITE
        Cells[6][11] = IWHITE
        Cells[6][12] = IWHITE

        Cells[30][9] = IWHITE
        Cells[31][9] = IWHITE
        Cells[32][9] = IWHITE
        Cells[33][9] = IWHITE
        Cells[34][9] = IWHITE
        Cells[35][9] = IWHITE
        Cells[36][9] = IWHITE
        Cells[37][9] = IWHITE
        Cells[30][10] = IWHITE
        Cells[32][10] = IWHITE
        Cells[33][10] = IWHITE
        Cells[34][10] = IWHITE
        Cells[35][10] = IWHITE
        Cells[37][10] = IWHITE
        Cells[30][11] = IWHITE
        Cells[31][11] = IWHITE
        Cells[32][11] = IWHITE
        Cells[33][11] = IWHITE
        Cells[34][11] = IWHITE
        Cells[35][11] = IWHITE
        Cells[36][11] = IWHITE
        Cells[37][11] = IWHITE


def main():
    global gamestate
    global pattern
    global randomPattern
    pygame.init()
    pygame.joystick.init()
    clock = pygame.time.Clock()
    
    resetGame()

    while True:
        for pgevent in pygame.event.get():
            event = process_event(pgevent)
            # if event.button == EXIT:
            #     pygame.quit()
            #     sys.exit()

            if event.type == PUSH:
                if event.button == UP:
                    resetGame()
                elif event.button == DOWN:
                    pass
                elif event.button == LEFT:
                    if pattern > 0:
                        pattern -= 1
                    resetGame()
                elif event.button == RIGHT:
                    if pattern < 2:
                        pattern += 1
                    resetGame()
                elif event.button == B1:
                    if gamestate == 0:
                        gamestate = 1
                    else:
                        gamestate = 0
                elif event.button == P1:
                    pygame.quit()
                    sys.exit()

        if gamestate == 1:
            CheckCells()
            pygame.surfarray.blit_array(screen, Cells)
            if randomPattern:
                gamestate = 0
                randomPattern = False
        else:
            if pattern > 0 and not randomPattern:
                gamestate = 1

        simDisplay.update(screen)
        ledDisplay.update(screen)

        clock.tick(10)

main()

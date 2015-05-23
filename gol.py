import pygame, led, sys, os, random, csv
import numpy
from pygame.locals import *
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
Cells[1][0] = IWHITE
Cells[2][1] = IWHITE
Cells[0][2] = IWHITE
Cells[1][2] = IWHITE
Cells[2][2] = IWHITE


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
    pass

def main():
    global gamestate
    pygame.init()
    clock = pygame.time.Clock()
    
    resetGame()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    pass
                elif event.key == K_DOWN:
                    pass
                elif event.key == K_LEFT:
                    pass
                elif event.key == K_RIGHT:
                    pass
                elif event.key == K_SPACE:
                    if gamestate == 0:
                        gamestate = 1
                    else:
                        CheckCells()
                        # print CountLifeNeighbours(11, 11)
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif event.type == KEYUP:
                if event.key == K_UP or event.key == K_DOWN:
                    pass

        if gamestate == 1:
            # screen.fill(BLACK)
            pygame.surfarray.blit_array(screen, Cells)

        else:
            pass

        simDisplay.update(screen)
        ledDisplay.update(screen)

        clock.tick(10)

main()

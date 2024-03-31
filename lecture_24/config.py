import pygame as pg


pg.font.init()
SYS_FONT = pg.font.SysFont(None, 25)

CELL_SIZE = 20
CELL = (CELL_SIZE, CELL_SIZE)
STEP = 20
SCREEN_W = CELL_SIZE * 50
SCREEN_H = CELL_SIZE * 30
SPEED = 4

colors = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (50, 130, 255)
}


#  directions
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

directions = {
    "start": (0, 0),
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0)
}

degrees = {
    "up": 0,
    "down": 180,
    "right": 90,
    "left": 270
}

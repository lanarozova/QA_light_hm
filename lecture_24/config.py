import pygame as pg


pg.font.init()
SYS_FONT = pg.font.SysFont(None, 35)

CELL_SIZE = 20
CELL = (CELL_SIZE, CELL_SIZE)
STEP = 20
SCREEN_W = CELL_SIZE * 30
SCREEN_H = CELL_SIZE * 20

colors = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (50, 130, 255),
    "white": (255, 255, 255)
}


scrn_colors = {
    "red": (255, 102, 102),
    "orange": (255, 178, 102),
    "yellow": (255, 255, 102),
    "lime": (178, 255, 102),
    "green": (102, 255, 102),
    "aqua": (102, 255, 178)
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


folder = "images"
images = {
    "snake": "head_up.png",
    "body": "body_vertical.png",
    "body_angle": "body_downright.png",
    "apple": "apple.png",
    "game_over": "game_over.png",
    "tail": "tail_down.png"
}

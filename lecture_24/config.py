from typing import NamedTuple

import pygame as pg


pg.font.init()

# default font
SYS_FONT = pg.font.SysFont(None, 45)

# screen parameters
CELL_SIZE = 20
CELL = (CELL_SIZE, CELL_SIZE)
STEP = 20
SCREEN_W = CELL_SIZE * 30
SCREEN_H = CELL_SIZE * 20

# directions
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

directions = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0)
}


# colors and images
class Colors(NamedTuple):
    orange: tuple
    yellow: tuple
    lime: tuple
    green: tuple
    aqua: tuple


class Images(NamedTuple):
    head: str
    body: str
    body_angle: str
    tail: str
    apple: str
    game_over: str


WHITE = (255, 255, 255)
DARK_GRAY = (150, 150, 150)
GRAY = (96, 96, 96)
RED = (255, 0, 0)
scrn_colors = Colors((255, 178, 102), (255, 255, 102), (178, 255, 102), (102, 255, 102), (102, 255, 178))

folder = "images"
sounds = "sounds"
images = Images("head_up.png", "body_vertical.png", "body_downright.png", "tail_down.png", "apple.png", "game_over.png")






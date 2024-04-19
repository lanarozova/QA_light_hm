from enum import Enum
from typing import NamedTuple

import pygame as pg
from os import path

pg.init()
pg.mixer.init()
pg.font.init()

# FONT
SYS_FONT = pg.font.SysFont(None, 45)
SYS_FONT.bold = True

# SCREEN PARAMS
CELL_SIZE = 20
CELL = (CELL_SIZE, CELL_SIZE)
STEP = 20
SCREEN_W = CELL_SIZE * 30
SCREEN_H = CELL_SIZE * 20

# DIRECTIONS
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


# GAME STATES
class States(Enum):
    START = 2
    PAUSE = 3
    PLAY = 4
    GAME_OVER = 5


#  IMAGES
class Images(NamedTuple):
    head: str
    body: str
    body_angle: str
    tail: str
    apple: str
    game_over: str
    start_screen: str


folder = "images"
images = Images(
    "head_up.png",
    "body_vertical.png",
    "body_downright.png",
    "tail_down.png",
    "apple.png",
    "game_over.png",
    "start_screen_im.png"
)


#  SOUNDS
sounds_folder = "sounds"


class Sounds(NamedTuple):
    crash: pg.mixer.Sound
    ooh: pg.mixer.Sound
    apple_eaten: pg.mixer.Sound
    level_up: pg.mixer.Sound


sounds = Sounds(pg.mixer.Sound(path.join(sounds_folder, "doorhit.mp3")),
                pg.mixer.Sound(path.join(sounds_folder, "ooh.mp3")),
                pg.mixer.Sound(path.join(sounds_folder, "eating-sound-effect.mp3")),
                pg.mixer.Sound(path.join(sounds_folder, "game-bonus.mp3")))


pg.mixer.music.load(path.join(sounds_folder, "spring-birds.mp3"))

# crash = pg.mixer.Sound(path.join(sounds, "doorhit.mp3"))
# OOH = pg.mixer.Sound(path.join(sounds, "ooh.mp3"))
# APPLE_EATEN = pg.mixer.Sound(path.join(sounds, "eating-sound-effect.mp3"))
# LEVEL_UP = pg.mixer.Sound(path.join(sounds, "game-bonus.mp3"))


#  COLORS
class ScrnColors(NamedTuple):
    orange: tuple
    yellow: tuple
    lime: tuple
    green: tuple
    aqua: tuple


class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DARK_GRAY = (150, 150, 150)
    GRAY = (96, 96, 96)
    RED = (202, 83, 41)


scrn_colors = ScrnColors((255, 178, 102), (255, 255, 102), (178, 255, 102), (102, 255, 102), (102, 255, 178))






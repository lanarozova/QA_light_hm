import pygame as pg


colors = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (50, 130, 255)
}


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


# SYS_FONT = pg.font.SysFont(25)

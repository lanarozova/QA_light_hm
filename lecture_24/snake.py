import pygame as pg
from info import colors
from screen import screen, draw_grid
from os import path
import sys

pg.init()

CELL = 20
STEP = 20
SCREEN_W = CELL * 50
SCREEN_H = CELL * 30
SPEED = 8

# direction
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

clock = pg.time.Clock()


class SnakeElement:

    def __init__(self, x, y, size: tuple, image):
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.size = size
        self.surface = pg.image.load(image).convert_alpha()
        self.surface = pg.transform.scale(self.surface, size)
        self.rect = self.surface.get_rect(x=x, y=y)
        self.element = (self.surface, self.rect)
        self.degree = 0

    def get_element(self):
        return self.element

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def rotate(self, desired):
        degrees = [0, 90, 180, 270]
        degree = None
        if desired in degrees and desired != self.degree:
            if desired > self.degree:
                degree = desired - self.degree
            if desired < self.degree:
                degree = 360 - self.degree + desired
            self.surface = pg.transform.rotate(self.surface, -degree)
            self.degree = desired


if __name__ == "__main__":
    screen = screen(SCREEN_W, SCREEN_H, colors["black"])
    head = SnakeElement(SCREEN_W // 2, SCREEN_H // 2, (CELL, CELL), path.join("images", "snake.png"))
    body_1 = SnakeElement(SCREEN_W // 2, SCREEN_H // 2 + CELL, (CELL, CELL), path.join("images", "body.png"))
    body_2 = SnakeElement(SCREEN_W // 2, SCREEN_H // 2 + CELL * 2, (CELL, CELL), path.join("images", "body.png"))
    snake = [head, body_1, body_2]


    direction = directions["start"]
    running = True
    pg.display.flip()
    while running:
        # screen.fill(colors["black"])
        for event in pg.event.get():

            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN and head.degree != degrees["up"]:
                    direction = directions["down"]
                    head.rotate(degrees["down"])
                    print(head.degree)
                if event.key == pg.K_UP and head.degree != degrees["down"]:
                    direction = directions["up"]
                    head.rotate(degrees["up"])
                    print(head.degree)
                if event.key == pg.K_RIGHT and head.degree != degrees["left"]:
                    direction = directions["right"]
                    head.rotate(degrees["right"])
                    print(head.degree)
                if event.key == pg.K_LEFT and head.degree != degrees["right"]:
                    direction = directions["left"]
                    head.rotate(degrees["left"])
                    print(head.degree)

        offset_x = STEP * direction[0]
        offset_y = STEP * direction[1]
        head.move(offset_x, offset_y)
        screen.fill(colors["black"])
        draw_grid(screen, cell_size=CELL)
        screen.blit(head.surface, head.rect)
        screen.blit(body_1.surface, body_1.rect)
        screen.blit(body_2.surface, body_2.rect)
        clock.tick(SPEED)
        pg.display.flip()


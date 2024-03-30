import pygame as pg
from info import colors, directions, degrees
from screen import screen, draw_grid
from os import path
import sys

pg.init()

CELL = 20
STEP = 20
SCREEN_W = CELL * 50
SCREEN_H = CELL * 30
SPEED = 8

#  directions
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"


class Apple:
    pass


class SnakeElement:

    def __init__(self, x, y, size: tuple, image):
        self.size = size
        self.surface = pg.image.load(image).convert_alpha()
        self.surface = pg.transform.scale(self.surface, size)
        self.rect = self.surface.get_rect(x=x, y=y)
        self.element = (self.surface, self.rect)
        self.degree = 0

    def get_element(self):
        return self.element

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_pos(self):
        return self.rect.x, self.rect.y

    # step is used here, need to change to accept coordinates after I figure out how to calc them
    def move(self, offset: list):
        self.rect.x += offset[0]
        self.rect.y += offset[1]

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def rotate(self, desired):
        angles = [0, 90, 180, 270]
        degree = None
        if desired in angles and desired != self.degree:
            if desired > self.degree:
                degree = desired - self.degree
            if desired < self.degree:
                degree = 360 - self.degree + desired
            self.surface = pg.transform.rotate(self.surface, -degree)
            self.degree = desired


class Snake:

    def __init__(self, head: SnakeElement):
        self.head = head
        self.body = []
        self.body.append(self.head)

    def __len__(self):
        return len(self.body)

    def extend(self, body_el: SnakeElement):
        self.body.append(body_el)

    def get_positions(self):
        positions = []
        for element in self.body:
            positions.append(element.get_pos())
        return positions

    def move(self, offset):
        next_x, next_y = self.head.get_x(), self.head.get_y()

        self.head.move(offset)

        for element in self.body[1:]:
            temp_x, temp_y = element.get_x(), element.get_y()
            element.set_position(next_x, next_y)
            next_x, next_y = temp_x, temp_y

        # print([element.get_pos() for element in self.body])


if __name__ == "__main__":
    screen = screen(SCREEN_W, SCREEN_H, colors["black"])

    #  snake creation
    head = SnakeElement(SCREEN_W // 2, SCREEN_H // 2, (CELL, CELL), path.join("images", "snake.png"))
    body_1 = SnakeElement(SCREEN_W // 2, SCREEN_H // 2 + CELL, (CELL, CELL), path.join("images", "body.png"))
    body_2 = SnakeElement(SCREEN_W // 2, SCREEN_H // 2 + CELL * 2, (CELL, CELL), path.join("images", "body.png"))
    snake = Snake(head)
    snake.extend(body_1)
    snake.extend(body_2)

    #  game logic
    clock = pg.time.Clock()
    direction = ""
    running = True
    curr_offset = [0, 0]
    for el in snake.body:
        screen.blit(el.surface, el.rect)

    while running:

        for event in pg.event.get():

            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN and head.degree != degrees[UP]:
                    direction = DOWN
                if event.key == pg.K_UP and head.degree != degrees[DOWN]:
                    direction = UP
                if event.key == pg.K_RIGHT and head.degree != degrees[LEFT]:
                    direction = RIGHT
                if event.key == pg.K_LEFT and head.degree != degrees[RIGHT]:
                    direction = LEFT

                angle = degrees[direction]
                snake.head.rotate(angle)
                curr_offset[0] = STEP * directions[direction][0]
                curr_offset[1] = STEP * directions[direction][1]
                # snake.move(curr_offset)

        snake.move(curr_offset)

        # head.rotate(degrees[direction])
        # head.move(offset_x, offset_y)
        # head.rotate(degrees[direction])
        # snake.move(offset_x, offset_y)
        screen.fill(colors["black"])
        draw_grid(screen, cell_size=CELL)

        #  placing objects on the screen, updating
        for el in snake.body:
            screen.blit(el.surface, el.rect)
        pg.display.flip()
        clock.tick(SPEED)


# import pygame as pg
# import os
# from game_setup import colors
#
# pg.init()
#
# GRID_CELL = 20
# SCREEN_W = GRID_CELL * 50 # + GRID_CELL * 50 / GRID_CELL
# SCREEN_H = GRID_CELL * 30 # + GRID_CELL * 30 / GRID_CELL
# STEP = 20
#
# # direction
# UP = (0 * STEP, -1 * STEP)
# DOWN = (0 * STEP, 1 * STEP)
# LEFT = (-1 * STEP, 0 * STEP)
# RIGHT = (1 * STEP, 0 * STEP)
#
# screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
# screen.fill(colors["black"])
#
#
# def draw_grid(scrn: pg.Surface, cell_size):
#     number_of_lines = scrn.get_width() // cell_size
#     start = [cell_size, scrn.get_width()]
#     end = [cell_size, 0]
#
#     # start = [scrn.get_width(), cell_size]
#     # end = [0, cell_size]
#     for i in range(number_of_lines):
#         pg.draw.line(scrn, (108, 108, 108), start, end)
#         start[1] += cell_size
#         end[1] += cell_size
#
#     # start = [cell_size, scrn.get_width()]
#     # end = [cell_size, 0]
#     for i in range(number_of_lines):
#         pg.draw.line(scrn, (108, 108, 108), start, end)
#         start[0] += cell_size
#         end[0] += cell_size
#
#
#
# surface = pg.image.load("images/snake.png").convert_alpha()
# surface = pg.transform.scale(surface, (20, 20))
# rect = surface.get_rect(x=screen.get_height() // 2, y=screen.get_width() // 2)
# surface = pg.transform.rotate(surface, 270.0)
# screen.blit(surface, rect)
# # draw_grid(screen, GRID_CELL)
#
# pg.draw.line(screen, (255, 255, 255), (SCREEN_W, 20), (0, 20))
# pg.display.flip()
#
# running = True
# direction = (0, 0)
# while running:
#
#     screen.fill(colors["black"])
#     keys = pg.key.get_pressed()
#     if keys[pg.K_LEFT]:
#         direction = LEFT
#         current_key = pg.K_LEFT
#     if keys[pg.K_RIGHT]:
#         direction = RIGHT
#         current_key = pg.K_RIGHT
#     if keys[pg.K_UP]:
#         direction = UP
#         current_key = pg.K_UP
#     if keys[pg.K_DOWN]:
#         direction = DOWN
#         current_key = pg.K_DOWN
#
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             running = False
#
#     rect.move_ip(direction)
#
#     draw_grid(screen, cell_size=GRID_CELL)
#     screen.blit(surface, rect)
#     pg.display.flip()


# class Button:
#
#     def __init__(self, x, y, w, h, text, colour):
#         self.button_surf = pg.Surface((w,h), 0, 24)
#         self.button_surf.fill(colour)
#         self.button = pg.Rect(x, y, w, h)
#         self.text_surf = SYS_FONT.render(text, False, (255,255,255))
#         # Pass the center coords of the button rect to the newly
#         # created text_rect for the purpose of centering the text.
#         self.text_rect = self.text_surf.get_rect(center=self.button.center)
#
#     def view(self, screen_surf):
#         screen_surf.blit(self.button_surf, self.button)
#         screen_surf.blit(self.text_surf, self.text_rect)
#

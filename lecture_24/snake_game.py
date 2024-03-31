from os import path
from config import *
import screen
from instances import GameElement, Worm, Apple


def play_game():
    pg.init()

    #  game instances creation
    game_scrn = screen.create(SCREEN_W, SCREEN_H, colors["black"])

    head = GameElement((SCREEN_W // 2, SCREEN_H // 2), CELL, image=path.join(folder, images["snake"]))
    worm = Worm(head)
    worm.extend()

    apple = Apple((0, 0), CELL, image=path.join(folder, images["apple"]))
    apple.set_new_random_pos(game_scrn, worm.get_positions())

    clock = pg.time.Clock()
    direction = ""
    running = True
    curr_offset = [0, 0]
    speed = 4

    while running:

        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_UP, pg.K_DOWN, pg.K_RIGHT, pg.K_LEFT]:
                    direction = worm.define_direction(event.key, direction)

        if direction:
            curr_offset[0] = STEP * directions[direction][0]
            curr_offset[1] = STEP * directions[direction][1]
            worm.move(curr_offset, direction)
            if worm.is_collision(apple.rect):
                worm.extend()
                apple.set_new_random_pos(game_scrn, worm.get_positions())
                speed += 1

        game_scrn.fill(colors["black"])
        screen.draw_grid(game_scrn, cell_size=CELL_SIZE)

        #  placing objects on the screen, updating
        apple.draw(game_scrn)
        worm.draw(game_scrn)
        pg.display.flip()
        clock.tick(speed)
        # counter += 1

    pg.quit()


if __name__ == "__main__":
    play_game()

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

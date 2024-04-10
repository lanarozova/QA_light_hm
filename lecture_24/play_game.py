from os import path
import sys
import random

from config import *
from snake.game_logic.screen import create, create_field, draw_game_over_screen
from snake.game_logic.logic import Snake, Apple
from cycle_generator import Cycle


def play_game():
    pg.init()

    #  game instances creation
    game_display = create(SCREEN_W, SCREEN_H)

    direction = random.choice([UP, DOWN, RIGHT, LEFT])
    snake = Snake(game_display, CELL, image=path.join(folder, images.head), direction=direction)

    apple = Apple(CELL, image=path.join(folder, images.apple))
    apple.set_new_random_pos(game_display, snake.get_positions())

    # other needed things
    paused = True
    clock = pg.time.Clock()
    curr_offset = [0, 0]
    speed = 4
    apple_counter = 0
    colors_gen = iter(Cycle([color for color in scrn_colors]))
    scrn_color = next(colors_gen)

    while True:
        events = pg.event.get()
        keys_pressed = 0
        for event in events:

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                keys_pressed += 1
                if event.key in [pg.K_UP, pg.K_DOWN, pg.K_RIGHT, pg.K_LEFT] and keys_pressed < 2:
                    paused = False
                    direction = snake.define_direction(event.key, direction)
                    snake.head.rotate(direction)
                elif event.key == pg.K_SPACE:
                    paused = not paused

        if not paused:
            curr_offset[0] = STEP * directions[direction][0]
            curr_offset[1] = STEP * directions[direction][1]
            snake.move(curr_offset)
            snake.calc_body_direction()

            # checking apple collision and changing scrn color / snake speed
            if snake.is_collision_with_another_el(apple.rect):
                snake.extend()
                apple.set_new_random_pos(game_display, snake.get_positions())
                apple_counter += 1
                if apple_counter % 5 == 0:
                    scrn_color = next(colors_gen)
                    speed += 1

            #  checking collisions with scrn borders or snake own body
            if snake.is_collision_with_own_body() or snake.is_collision_with_screen_border(game_display):
                draw_game_over_screen(game_display, apple_counter)
                pg.display.flip()
                pg.time.wait(1500)
                pg.quit()
                sys.exit()

        #  drawing screen
        game_display.fill(scrn_color)
        create_field(game_display, CELL, CELL_SIZE, GRAY)

        # placing game elements on the screen and updating display
        snake.update_images()
        apple.draw(game_display)
        snake.draw(game_display)
        pg.display.flip()
        clock.tick(speed)


if __name__ == "__main__":
    play_game()
    pg.quit()

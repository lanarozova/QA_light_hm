from os import path
import sys
import random

from config import *
from screen import create, draw_grid
from instances import Snake, Apple
from cycle_generator import Cycle


def play_game():
    pg.init()

    #  game instances creation
    game_display = create(SCREEN_W, SCREEN_H, colors["black"])

    direction = random.choice([UP, DOWN, RIGHT, LEFT])
    snake = Snake(game_display, CELL, image=path.join(folder, images["snake"]), direction=direction)

    apple = Apple(CELL, image=path.join(folder, images["apple"]))
    apple.set_new_random_pos(game_display, snake.get_positions())

    # other needed things
    paused = True
    clock = pg.time.Clock()
    curr_offset = [0, 0]
    speed = 4
    apple_counter = 0
    colors_gen = iter(Cycle([color for color in scrn_colors]))
    scrn_color = next(colors_gen)

    game_over = pg.image.load(path.join(folder, images["game_over"]))
    game_over = pg.transform.scale(game_over, (SCREEN_W, SCREEN_H))

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
                game_display.blit(game_over, (0, 0))
                go_text = SYS_FONT.render(f"YOUR SCORE IS {apple_counter}", True, colors["black"])
                go_text_rect = go_text.get_rect()
                go_text_rect.center = (SCREEN_W / 2, SCREEN_H / 8)
                game_display.blit(go_text, go_text_rect)
                pg.display.flip()
                pg.time.wait(1500)
                pg.quit()
                sys.exit()

        #  drawing screen
        game_display.fill(scrn_colors[scrn_color])
        draw_grid(game_display, CELL_SIZE)

        # placing game elements on the screen and updating display
        apple.draw(game_display)
        snake.draw(game_display)
        pg.display.flip()
        clock.tick(speed)


if __name__ == "__main__":
    play_game()
    pg.quit()

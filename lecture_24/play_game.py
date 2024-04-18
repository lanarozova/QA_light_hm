from os import path
import sys
import random

from config import *
from lecture_24.game_logic.screen import create, create_field, draw_game_over_screen
from lecture_24.game_logic.snake import Snake
from lecture_24.game_logic.apple import Apple
from lecture_24.cycle_generator import Cycle
from lecture_24.game_logic.button import Button


pg.init()
pg.font.init()
pg.mixer.init()


def play_game():
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

    # sounds
    pg.mixer.music.load(path.join(sounds, 'spring-birds.mp3'))
    pg.mixer.music.play(-1)
    crash_sound = pg.mixer.Sound(path.join(sounds, "clank-car-crash-collision.mp3"))
    apple_eaten = pg.mixer.Sound(path.join(sounds, "eating-sound-effect.mp3"))
    game_level_up = pg.mixer.Sound(path.join(sounds, "game-bonus.mp3"))

    while True:
        events = pg.event.get()
        keys_pressed = 0
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = event.pos
                pass

            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif event.type == pg.KEYDOWN:
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
                pg.mixer.Sound.play(apple_eaten)
                snake.extend()
                apple.set_new_random_pos(game_display, snake.get_positions())
                apple_counter += 1
                if apple_counter % 5 == 0:
                    pg.mixer.Sound.play(game_level_up)
                    scrn_color = next(colors_gen)
                    speed += 1

            #  checking collisions with scrn borders or snake own body
            if snake.is_collision_with_own_body() or snake.is_collision_with_screen_border(game_display):
                pg.mixer.music.stop()
                pg.mixer.Sound.play(crash_sound)
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

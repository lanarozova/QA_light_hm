import sys
import random

from config import *
from lecture_24.game_logic.screen import (create,
                                          create_field,
                                          draw_gray_screen,
                                          display_game_over_message,
                                          display_score,
                                          play_game_button,
                                          resume_button,
                                          restart_button,
                                          quit_button)
from lecture_24.game_logic.snake import Snake
from lecture_24.game_logic.apple import Apple
from lecture_24.cycle_generator import Cycle


def main():
    #  game instances creation
    game_display = create(SCREEN_W, SCREEN_H)

    direction = random.choice([UP, DOWN, RIGHT, LEFT])
    snake = Snake(game_display, CELL, image=path.join(folder, images.head), direction=direction)

    apple = Apple(CELL, image=path.join(folder, images.apple))
    apple.set_new_random_pos(game_display, snake.get_positions())

    # game start setup
    state = States.START
    game_paused = True
    clock = pg.time.Clock()
    curr_offset = [0, 0]
    speed = 4
    apple_counter = 0
    colors_gen = iter(Cycle([color for color in scrn_colors]))
    scrn_color = next(colors_gen)
    pg.mixer.music.play(-1)
    pg.mixer.music.pause()

    main_image_surf = pg.image.load(path.join(folder, images.start_screen))
    main_image_surf = pg.transform.scale(main_image_surf, (CELL_SIZE * 20, CELL_SIZE * 20))
    main_image_surf.convert_alpha()
    main_image_rect = main_image_surf.get_rect(topleft=(100, -100))

    while True:
        # event = pg.event.wait()
        events = pg.event.get()
        keys_pressed = 0
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = event.pos
                if state == States.START and play_game_button.button.collidepoint(x, y):
                    state = States.PLAY
                    pg.mixer.music.unpause()
                elif state == States.PAUSE and resume_button.button.collidepoint(x, y):
                    state = States.PLAY
                    pg.mixer.music.unpause()
                    game_paused = False
                elif quit_button.button.collidepoint(x, y):
                    pg.quit()
                    sys.exit()
                elif state in (States.PAUSE, States.GAME_OVER) and restart_button.button.collidepoint(x, y):
                    direction = random.choice([UP, DOWN, RIGHT, LEFT])
                    snake = Snake(game_display, CELL, image=path.join(folder, images.head), direction=direction)
                    apple.set_new_random_pos(game_display, snake.get_positions())
                    apple_counter = 0
                    speed = 4
                    state = States.PLAY
                    game_paused = True
                    pg.mixer.music.play(-1)

            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif event.type == pg.KEYDOWN:
                keys_pressed += 1
                if event.key in [pg.K_UP, pg.K_DOWN, pg.K_RIGHT, pg.K_LEFT] and keys_pressed < 2:
                    game_paused = False
                    state = States.PLAY
                    direction = snake.define_direction(event.key, direction)
                    snake.head.rotate(direction)
                elif event.key == pg.K_SPACE:
                    state = States.PAUSE
                    pg.mixer.music.pause()
                    game_paused = True

        if not game_paused:
            curr_offset[0] = STEP * directions[direction][0]
            curr_offset[1] = STEP * directions[direction][1]
            snake.move(curr_offset)
            snake.calc_body_direction()

            # checking apple collision and changing scrn color / snake speed
            if snake.is_collision_with_another_el(apple.rect):
                pg.mixer.Sound.play(sounds.apple_eaten)
                snake.extend()
                apple.set_new_random_pos(game_display, snake.get_positions())
                apple_counter += 1
                if apple_counter % 5 == 0:
                    pg.mixer.Sound.play(sounds.level_up)
                    scrn_color = next(colors_gen)
                    speed += 1

            #  checking collisions with scrn borders or snake own body
            if snake.is_collision_with_own_body() or snake.is_collision_with_screen_border(game_display):
                pg.mixer.music.stop()
                pg.mixer.Sound.play(sounds.crash)
                pg.mixer.Sound.play(sounds.ooh)
                game_paused = True
                state = States.GAME_OVER

        #  drawing screen
        if state == States.START:
            draw_gray_screen(game_display)
            play_game_button.draw(game_display)
            quit_button.draw(game_display)
            game_display.blit(main_image_surf, main_image_rect)

        elif state == States.PLAY:
            game_display.fill(scrn_color)
            create_field(game_display, CELL, CELL_SIZE, Colors.GRAY)
            snake.update_images()
            apple.draw(game_display)
            snake.draw(game_display)

        elif state == States.PAUSE:
            draw_gray_screen(game_display)
            resume_button.draw(game_display)
            restart_button.draw(game_display)
            quit_button.draw(game_display)

        elif state == States.GAME_OVER:
            draw_gray_screen(game_display)
            display_score(game_display, apple_counter)
            display_game_over_message(game_display)
            restart_button.draw(game_display)
            quit_button.draw(game_display)

        else:
            pass

        pg.display.flip()
        clock.tick(speed)


if __name__ == "__main__":
    main()

from lecture_24.config import *
from lecture_24.game_logic.game_element import GameElement
from lecture_24.game_logic.button import Button


def create(h: int, w: int) -> pg.Surface:
    scrn = pg.display.set_mode((h, w))
    # scrn.fill(color)
    return scrn


def draw_grid(scrn: pg.Surface, cell_size: int) -> None:
    lines_x = (scrn.get_width() // cell_size)
    lines_y = scrn.get_height() // cell_size
    lines = [lines_x, lines_y]
    color = (90, 90, 90)

    start = [cell_size, 0]
    end = [cell_size, scrn.get_height()]

    for i, number_of_lines in enumerate(lines):
        for _ in range(number_of_lines):
            pg.draw.line(scrn, color, start, end)
            start[i] += cell_size
            end[i] += cell_size

        start = [scrn.get_width(), cell_size]
        end = [0, cell_size]


def create_field(scrn: pg.Surface, cell: tuple[int], cell_size, color):
    lines_x = scrn.get_width() // cell_size
    lines_y = scrn.get_width() // cell_size
    field = []

    y = 0
    for i in range(lines_y):
        if i % 2 == 0:
            x = 0
        else:
            x = 20

        for j in range(lines_x):
            field_element = GameElement((x, y), cell, color=color)
            field.append(field_element)
            x += 40
        y += 20

    for el in field:
        el.draw(scrn)


def draw_gray_screen(scrn: pg.Surface):
    scrn.fill(Colors.DARK_GRAY)
    create_field(scrn, CELL, CELL_SIZE, Colors.WHITE)


def display_score(scrn: pg.Surface, game_score):
    width = scrn.get_width()
    height = scrn.get_height()
    score = Button(
        width // 6,
        height // 4,
        CELL_SIZE * 20,
        CELL_SIZE * 2,
        f"YOUR SCORE IS {game_score}",
        Colors.BLACK,
        Colors.RED)
    score.draw(scrn)


def display_game_over_message(scrn: pg.Surface):
    width = scrn.get_width()
    height = scrn.get_height()

    game_over = Button(
        width // 6,
        height // 10,
        CELL_SIZE * 20,
        CELL_SIZE * 2,
        "GAME OVER",
        Colors.BLACK,
        Colors.RED)
    game_over.draw(scrn)


# BUTTONS
play_game_button = Button(
    SCREEN_W // 6,
    SCREEN_H // 2,
    CELL_SIZE * 20,
    CELL_SIZE * 2,
    "PLAY",
    Colors.BLACK,
    Colors.WHITE)
quit_button = Button(
    SCREEN_W // 6,
    SCREEN_H // 1.425,
    CELL_SIZE * 20,
    CELL_SIZE * 2,
    "QUIT",
    Colors.BLACK,
    Colors.WHITE)
restart_button = Button(
    SCREEN_W // 6,
    SCREEN_H // 2,
    CELL_SIZE * 20,
    CELL_SIZE * 2,
    "RESTART",
    Colors.BLACK,
    Colors.WHITE)
resume_button = Button(
    SCREEN_W // 6,
    SCREEN_H // 3.325,
    CELL_SIZE * 20,
    CELL_SIZE * 2,
    f"RESUME",
    Colors.BLACK,
    Colors.WHITE)







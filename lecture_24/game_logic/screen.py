from config import *
from lecture_24.game_logic.game_element import GameElement


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


def draw_game_over_screen(scrn: pg.Surface, game_score):
    width = scrn.get_width()
    height = scrn.get_height()

    scrn.fill(DARK_GRAY)
    create_field(scrn, CELL, CELL_SIZE, WHITE)

    SYS_FONT.bold = True

    score_text = SYS_FONT.render(f"YOUR SCORE IS {game_score}", True, RED)
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (width / 2, height / 7.3)

    go_text = SYS_FONT.render(f"GAME OVER", True, RED)
    go_text_rect = go_text.get_rect()
    go_text_rect.center = (width / 2, height / 2.26)

    scrn.blit(go_text, go_text_rect)
    scrn.blit(score_text, score_text_rect)

import pygame as pg


def screen(h, w, color):
    scrn = pg.display.set_mode((h, w))
    scrn.fill(color)
    return scrn


def draw_grid(scrn: pg.Surface, cell_size):
    number_of_lines = scrn.get_width() // cell_size
    color = (90, 90, 90)

    start = [cell_size, scrn.get_width()]
    end = [cell_size, 0]

    for i in range(2):

        for _ in range(number_of_lines):
            pg.draw.line(scrn, color, start, end)
            start[i] += cell_size
            end[i] += cell_size

        start = [scrn.get_width(), cell_size]
        end = [0, cell_size]


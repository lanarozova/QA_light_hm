from config import pg


def create(h: int, w: int, color: tuple) -> pg.Surface:
    scrn = pg.display.set_mode((h, w))
    scrn.fill(color)
    return scrn


def draw_grid(scrn: pg.Surface, cell_size: int) -> None:
    number_of_lines_x = (scrn.get_width() // cell_size)
    number_of_lines_y = scrn.get_height() // cell_size
    lines = [number_of_lines_x, number_of_lines_y]
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

# TODO: create field in green colors and chess order of the rectangles
# def draw_field(scrn: pg.Surface, cell_size):
#     pass


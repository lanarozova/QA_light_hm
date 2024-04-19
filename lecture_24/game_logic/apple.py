from lecture_24.config import *
from lecture_24.game_logic.game_element import GameElement


class Apple(GameElement):

    def __init__(self, size: tuple, image: str, pos: tuple = (0, 0)):
        super().__init__(pos, size, image)

    def set_new_random_pos(self, scrn: pg.Surface, snake_positions: list[tuple]) -> None:
        new_pos = Apple.generate_random_pos(scrn.get_width(), scrn.get_height(), CELL_SIZE)
        taken = new_pos in snake_positions
        while taken and new_pos != self.get_pos():
            new_pos = Apple.generate_random_pos(scrn.get_width(), scrn.get_height(), CELL_SIZE)
        self.set_pos(new_pos)

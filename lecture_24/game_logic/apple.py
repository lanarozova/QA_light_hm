from lecture_24.config import *
from lecture_24.game_logic.game_element import GameElement


class Apple(GameElement):

    def __init__(self, size: tuple, image: str, pos: tuple = (0, 0)):
        super().__init__(pos, size, image)

    @staticmethod
    def is_new_pos_taken(worm_positions: list[tuple], new_pos: tuple) -> bool:
        for pos in worm_positions:
            if pos == new_pos:
                return True
            else:
                return False

    def set_new_random_pos(self, scrn: pg.Surface, snake_positions: list[tuple]) -> None:
        new_pos = Apple.generate_random_pos(scrn.get_width(), scrn.get_height(), CELL_SIZE)
        taken = Apple.is_new_pos_taken(snake_positions, new_pos)
        while taken and new_pos != self.get_pos():
            new_pos = Apple.generate_random_pos(scrn.get_width(), scrn.get_height(), CELL_SIZE)
        self.set_pos(new_pos)

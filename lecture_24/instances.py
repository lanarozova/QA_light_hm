from os import path
from config import *
import random


class GameElement:

    def __init__(
            self,
            pos: tuple,
            size: tuple,
            image: str = "",
            color: str = "",
            direction: str = "up"
    ) -> None:

        if image or color:
            self.size = size
            self.direction = "up"
            if image:
                self.surface = pg.image.load(image).convert_alpha()
                self.surface = pg.transform.scale(self.surface, size)
                self.rect = self.surface.get_rect(x=pos[0], y=pos[1])
            elif color:
                self.surface = pg.Surface(self.size)
                self.rect = self.surface.get_rect(x=pos[0], y=pos[1])
            if self.direction != direction:
                self.rotate(direction)

        else:
            raise TypeError("Insufficient arguments to create a class object. Image or color is necessary.")

    def get_pos(self) -> tuple:
        return self.rect.x, self.rect.y

    # step is used here, need to change to accept coordinates after I figure out how to calc them
    def move(self, offset: list) -> None:
        self.rect.x += offset[0]
        self.rect.y += offset[1]

    def draw(self, scrn: pg.Surface) -> None:
        scrn.blit(self.surface, self.rect)

    def set_pos(self, pos: tuple) -> None:
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def rotate(self, direction: str) -> None:
        degrees = {
            "up": 0,
            "left": 270,
            "down": 180,
            "right": 90
        }
        rotate_degree = None
        required_degree = degrees[direction]
        current_degree = degrees[self.direction]

        if direction in degrees and degrees[direction] != current_degree:
            if required_degree > current_degree:
                rotate_degree = required_degree - current_degree
            if degrees[direction] < current_degree:
                rotate_degree = 360 - current_degree + required_degree

            self.surface = pg.transform.rotate(self.surface, -rotate_degree)
            self.direction = direction

    @staticmethod
    def generate_random_pos(
            scrn_width: int,
            scrn_height: int,
            cell_size: int
    ) -> tuple:

        x = random.randrange(0, scrn_width, cell_size)
        y = random.randrange(0, scrn_height, cell_size)
        return x, y


class Snake:

    def __init__(
            self,
            scrn: pg.Surface,
            size: tuple,
            pos: tuple = (0, 0),
            image: str = "",
            color: str = "",
            direction: str = "up",
            length: int = 3
    ) -> None:

        self.head = GameElement(pos, size, image, color, direction)
        self.body = [self.head]
        self.length = length
        self.set_random_pos(scrn, CELL_SIZE)
        for _ in range(self.length - 1):
            self.extend()

    def get_positions(self) -> list:
        positions = []
        for element in self.body:
            positions.append(element.get_pos())
        return positions

    def set_random_pos(self, scrn: pg.Surface, cell_size: int) -> None:
        screen_w = scrn.get_width()
        screen_h = scrn.get_height()
        min_x = min_y = max_x = max_y = 0
        if self.head.direction == UP:
            min_y = 0
            max_y = screen_h - cell_size * self.length
        if self.head.direction == DOWN:
            min_y = 0 + cell_size * self.length
            max_y = screen_h - cell_size
        if self.head.direction == RIGHT:
            min_x = 0 + cell_size * self.length
            max_x = screen_w - cell_size
        if self.head.direction == LEFT:
            min_x = 0
            max_x = screen_w - cell_size * self.length

        new_pos = GameElement.generate_random_pos(screen_w, screen_h, cell_size)
        while new_pos[0] not in range(min_x, max_x) and new_pos[1] not in range(min_y, max_y):
            new_pos = GameElement.generate_random_pos(screen_w, screen_h, cell_size)
        self.head.set_pos(new_pos)

    def define_direction(self, event_key: int, current_direction: str) -> str:
        direction = current_direction

        if event_key == pg.K_DOWN and self.head.direction != UP:
            direction = DOWN
        if event_key == pg.K_UP and self.head.direction != DOWN:
            direction = UP
        if event_key == pg.K_RIGHT and self.head.direction != LEFT:
            direction = RIGHT
        if event_key == pg.K_LEFT and self.head.direction != RIGHT:
            direction = LEFT
        return direction

    def calc_body_direction(self) -> None:
        prev_x, prev_y = self.head.rect.x, self.head.rect.y

        for i, el in enumerate(self.body):
            if el == self.head:
                continue

            element_direction = ""
            current_x, current_y = el.get_pos()
            delta_x = prev_x - current_x
            delta_y = prev_y - current_y
            if delta_x == STEP:
                element_direction = RIGHT
            elif delta_x == -STEP:
                element_direction = LEFT
            elif delta_y == STEP:
                element_direction = DOWN
            elif delta_y == -STEP:
                element_direction = UP
            else:
                pass
            prev_x, prev_y = current_x, current_y

            el.rotate(element_direction)

    def move(self, offset: list) -> None:
        prev_x, prev_y = self.head.get_pos()

        for i, el in enumerate(self.body):

            if el == self.head:
                self.head.move(offset)
            else:
                current_x, current_y = el.get_pos()
                el.set_pos((prev_x, prev_y))
                prev_x, prev_y = current_x, current_y

    def draw(self, scrn: pg.Surface) -> None:
        for el in self.body:
            el.draw(scrn)

    def extend(self) -> None:
        next_body_el_pos = ()
        last_el = self.body[-1]
        if last_el.direction == UP:
            next_body_el_pos = last_el.rect.bottomleft[0], last_el.rect.bottomleft[1]
        if last_el.direction == DOWN:
            next_body_el_pos = last_el.rect.topleft[0], last_el.rect.topleft[1] - CELL_SIZE
        if last_el.direction == LEFT:
            next_body_el_pos = last_el.rect.topright[0], last_el.rect.topright[1]
        if last_el.direction == RIGHT:
            next_body_el_pos = last_el.rect.topleft[0] - CELL_SIZE, last_el.rect.topleft[1]

        next_body_el = GameElement(next_body_el_pos, CELL, image=path.join(folder, images["body"]))
        next_body_el.rotate(last_el.direction)
        self.body.append(next_body_el)

    def is_collision_with_another_el(self, game_el_rect: pg.Rect) -> bool:
        return self.head.rect.colliderect(game_el_rect)

    def is_collision_with_own_body(self) -> bool:
        for el in self.body[1:]:
            if self.head.rect.colliderect(el.rect):
                return True
        return False

    def is_collision_with_screen_border(self, scrn: pg.Surface) -> bool:
        width, height = scrn.get_width(), scrn.get_height()
        if self.head.rect.right < CELL_SIZE or self.head.rect.left > width - CELL_SIZE:
            return True
        if self.head.rect.top < 0 or self.head.rect.bottom > height:
            return True
        return False


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

    def set_new_random_pos(self, scrn: pg.Surface, worm_positions: list[tuple]) -> None:
        new_pos = Apple.generate_random_pos(scrn.get_width(), scrn.get_height(), CELL_SIZE)
        taken = Apple.is_new_pos_taken(worm_positions, new_pos)
        while taken and new_pos != self.get_pos():
            new_pos = Apple.generate_random_pos(scrn.get_width(), scrn.get_height(), CELL_SIZE)
        self.set_pos(new_pos)

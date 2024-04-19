from lecture_24.config import *
from lecture_24.game_logic.game_element import GameElement
from os import path


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

    def update_images(self):
        for i in range(1, len(self.body) - 1):
            next_el = self.body[i + 1]
            el = self.body[i]
            if el.direction == next_el.direction:
                el.update_image(path.join(folder, images.body))
                continue
            el.update_image(path.join(folder, images.body_angle))

            if el.direction == UP and next_el.direction == RIGHT:
                el.rotate(DOWN)
            elif el.direction == UP and next_el.direction == LEFT:
                el.rotate(LEFT)
            elif el.direction == DOWN and next_el.direction == RIGHT:
                el.rotate(RIGHT)
            elif el.direction == DOWN and next_el.direction == LEFT:
                el.rotate(UP)
            elif el.direction == LEFT and next_el.direction == UP:
                el.rotate(RIGHT)
            elif el.direction == LEFT and next_el.direction == DOWN:
                el.rotate(DOWN)
            elif el.direction == RIGHT and next_el.direction == UP:
                el.rotate(UP)
            elif el.direction == RIGHT and next_el.direction == DOWN:
                el.rotate(LEFT)
        tail = self.body[-1]
        tail.update_image(path.join(folder, images.tail))
        tail.rotate(tail.direction)

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

        next_body_el = GameElement(next_body_el_pos, CELL, image=path.join(folder, images.body))
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

from os import path
from config import *
import random


class GameElement:

    def __init__(self, pos: tuple, size: tuple, image="", color="", direction="up"):
        if image or color:
            self.size = size
            self.direction = direction
            if image:
                self.surface = pg.image.load(image).convert_alpha()
                self.surface = pg.transform.scale(self.surface, size)
                self.rect = self.surface.get_rect(x=pos[0], y=pos[1])
            if color:
                self.surface = pg.Surface(self.size)
                self.rect = self.surface.get_rect(x=pos[0], y=pos[1])

        else:
            raise TypeError("Insufficient arguments to create a class object. Image or color is necessary.")

    def get_pos(self):
        return self.rect.x, self.rect.y

    # step is used here, need to change to accept coordinates after I figure out how to calc them
    def move(self, offset: list):
        self.rect.x += offset[0]
        self.rect.y += offset[1]

    def draw(self, scrn):
        scrn.blit(self.surface, self.rect)

    def set_pos(self, pos: tuple):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def rotate(self, direction="up"):
        degrees = {"up": 0,
                  "left": 270,
                  "down": 180,
                  "right": 90}
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
    def generate_random_pos(scrn_width, scrn_height, cell_size: int):
        x = random.randrange(0, scrn_width, cell_size)
        y = random.randrange(0, scrn_height, cell_size)
        return x, y


class Snake:

    def __init__(self, head: GameElement):
        self.head = head
        self.body = []
        self.body.append(self.head)

    def __len__(self):
        return len(self.body)

    def get_positions(self):
        positions = []
        for element in self.body:
            positions.append(element.get_pos())
        return positions

    def define_direction(self, event_key, current_direction):
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

    def calc_body_direction(self):
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

    def move(self, offset):
        prev_x, prev_y = self.head.get_pos()

        for i, el in enumerate(self.body):

            if el == self.head:
                self.head.move(offset)
            else:
                current_x, current_y = el.get_pos()
                el.set_pos((prev_x, prev_y))
                prev_x, prev_y = current_x, current_y

    def draw(self, scrn):
        for el in self.body:
            el.draw(scrn)

    def extend(self):
        next_body_el_pos = ()
        last_el = self.body[-1]
        if last_el.direction == UP:
            next_body_el_pos = last_el.rect.bottomleft[0], last_el.rect.bottomleft[1]
        if last_el.direction == DOWN:
            next_body_el_pos = last_el.rect.topleft[0], last_el.rect.topleft[1] + CELL_SIZE
        if last_el.direction == LEFT:
            next_body_el_pos = last_el.rect.topright[0], last_el.rect.topright[1]
        if last_el.direction == RIGHT:
            next_body_el_pos = last_el.rect.topleft[0] - CELL_SIZE, last_el.rect.topleft[1]

        next_body_el = GameElement(next_body_el_pos, CELL, image=path.join(folder, images["body"]))
        next_body_el.rotate(last_el.direction)
        self.body.append(next_body_el)

    def is_collision_with_another_el(self, game_el_rect: pg.Rect):
        return self.head.rect.colliderect(game_el_rect)

    def is_collision_with_own_body(self):
        for el in self.body[1:]:
            if self.head.rect.colliderect(el.rect):
                return True
        return False

    def is_collision_with_screen_border(self, scrn: pg.Surface):
        width, height = scrn.get_width(), scrn.get_height()
        if self.head.rect.right < CELL_SIZE or self.head.rect.left > width - CELL_SIZE:
            return True
        if self.head.rect.top < 0 or self.head.rect.bottom > height:
            return True
        return False


class Apple(GameElement):

    def __init__(self, pos, size, image):
        super().__init__(pos, size, image)

    @staticmethod
    def is_new_pos_taken(worm_positions: list[tuple], new_pos: tuple):
        for pos in worm_positions:
            if pos == new_pos:
                return True
            else:
                return False

    def set_new_random_pos(self, scrn: pg.Surface, worm_positions: list[tuple], ):
        new_pos = Apple.generate_random_pos(scrn.get_width(), scrn.get_height(), CELL_SIZE)
        taken = Apple.is_new_pos_taken(worm_positions, new_pos)
        while taken and new_pos != self.get_pos():
            new_pos = Apple.generate_random_pos(scrn.get_width(), scrn.get_height(), CELL_SIZE)
        self.set_pos(new_pos)

from config import *
import random


class GameElement:

    def __init__(self, pos: tuple, size: tuple, image="", color=""):
        if image or color:
            self.size = size
            self.degree = 0
            if image:
                self.surface = pg.image.load(image).convert_alpha()
                self.surface = pg.transform.scale(self.surface, size)
                self.rect = self.surface.get_rect(x=pos[0], y=pos[1])
                self.element = (self.surface, self.rect)
            if color:
                self.surface = pg.Surface(self.size)
                self.rect = self.surface.get_rect(x=pos[0], y=pos[1])
                self.element = (self.surface, self.rect)
        else:
            raise TypeError("Insufficient arguments to create a class object. Image or color is necessary.")

    def get_element(self):
        return self.element

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

    def rotate(self, desired):
        angles = [0, 90, 180, 270]
        degree = None
        if desired in angles and desired != self.degree:
            if desired > self.degree:
                degree = desired - self.degree
            if desired < self.degree:
                degree = 360 - self.degree + desired
            self.surface = pg.transform.rotate(self.surface, -degree)
            self.degree = desired


class Worm:

    def __init__(self, head: GameElement):
        self.head = head
        self.body = []
        self.body.append(self.head)

    def __len__(self):
        return len(self.body)

    def extend(self, body_el: GameElement):
        self.body.append(body_el)

    def get_positions(self):
        positions = []
        for element in self.body:
            positions.append(element.get_pos())
        return positions

    def move(self, offset, angle):
        next_x, next_y = self.head.get_pos()

        for i, el in enumerate(self.body):

            if el == self.head:
                self.head.rotate(angle)
                self.head.move(offset)
            else:
                current_x, current_y = el.get_pos()
                if self.body[i-1].rect.x != el.rect.x and self.body[i-1].rect.y != el.rect.y:
                    el.rotate(angle)
                el.set_pos((next_x, next_y))
                next_x, next_y = current_x, current_y

    def define_direction(self, event_key):
        direction = ""
        if event_key == pg.K_DOWN and self.head.degree != degrees[UP]:
            direction = DOWN
        if event_key == pg.K_UP and self.head.degree != degrees[DOWN]:
            direction = UP
        if event_key == pg.K_RIGHT and self.head.degree != degrees[LEFT]:
            direction = RIGHT
        if event_key == pg.K_LEFT and self.head.degree != degrees[RIGHT]:
            direction = LEFT
        return direction

    def draw(self, scrn):
        for el in self.body:
            el.draw(scrn)


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

    @staticmethod
    def generate_new_pos(scrn: pg.Surface, cell_size: int):
        x = random.randrange(0, scrn.get_width(), cell_size)
        y = random.randrange(0, scrn.get_height(), cell_size)
        return x, y

    def set_new_random_pos(self, scrn: pg.Surface, worm_positions: list[tuple], ):
        new_pos = Apple.generate_new_pos(scrn, CELL_SIZE)
        taken = Apple.is_new_pos_taken(worm_positions, new_pos)
        while taken and new_pos != self.get_pos():
            new_pos = Apple.generate_new_pos(scrn, CELL_SIZE)
        self.set_pos(new_pos)



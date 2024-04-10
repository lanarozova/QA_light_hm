from lecture_24.config import *
import random


class GameElement:

    def __init__(
            self,
            pos: tuple,
            size: tuple,
            image: str = "",
            color: str | tuple = "",
            direction: str = "up"
    ) -> None:

        if image or color:
            self.size = size
            self.direction = "up"
            if image:
                self.surface = pg.image.load(image).convert_alpha()
                self.surface = pg.transform.scale(self.surface, self.size)
                self.rect = self.surface.get_rect(x=pos[0], y=pos[1])
            elif color:
                self.surface = (pg.Surface(self.size))
                self.surface.fill(color)
                self.surface.set_alpha(100)
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
        rotate_degree = 0
        required_degree = degrees[direction]
        current_degree = degrees[self.direction]

        if direction in degrees:
            if required_degree > current_degree:
                rotate_degree = required_degree - current_degree
            if required_degree < current_degree:
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

    def update_image(self, image):
        self.surface = pg.image.load(image).convert_alpha()
        self.surface = pg.transform.scale(self.surface, self.size)
        self.rect = self.surface.get_rect(x=self.rect.x, y=self.rect.y)
        temp_dir = self.direction
        self.direction = UP
        self.rotate(temp_dir)

from lecture_24.config import *


class Button:

    def __init__(self, x, y, w, h, text, colour):
        self.button_surf = pg.Surface((w, h), 0, 24)
        self.button_surf.fill(colour)
        self.button = pg.Rect(x, y, w, h)
        self.text_surf = SYS_FONT.render(text, False, (255, 255, 255))
        # Pass the center coords of the button rect to the newly
        # created text_rect for the purpose of centering the text.
        self.text_rect = self.text_surf.get_rect(center=self.button.center)

    def view(self, screen_surf):
        screen_surf.blit(self.button_surf, self.button)
        screen_surf.blit(self.text_surf, self.text_rect)


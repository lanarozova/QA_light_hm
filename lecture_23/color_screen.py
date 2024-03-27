import pygame
from cycle_generator import Cycle

from colors_texts_images import black, white, yellow, s_colors, dogs, texts


def initial_game_setup():
    pygame.init()


def create_screen(x: int, y: int, caption: str, color: tuple[int]) -> pygame.Surface:
    screen = pygame.display.set_mode((x, y))
    pygame.display.set_caption(caption)
    screen.fill(color)
    return screen


def load_images(images: list, screen: pygame.Surface) -> list[pygame.Surface]:
    loaded_images = []
    for image in images:
        loaded_images.append(pygame.image.load(image).convert_alpha(screen))
    return loaded_images


def create_text(
        f_color: tuple,
        bg_color: tuple,
        f_size: int,
        text_string: str,
        screen: pygame.Surface,
        center_div_koef: tuple,
        f_name: str = None
) -> tuple:
    font = pygame.font.Font(f_name, size=f_size)
    text = font.render(text_string, True, f_color, bg_color)
    text_rect = text.get_rect()
    text_rect.center = (screen.get_height() // center_div_koef[0], screen.get_width() // center_div_koef[1])
    return text, text_rect


def main():
    initial_game_setup()
    game_screen = create_screen(
        1000,
        600,
        'Pygame Mouse Click - Change Color And Feed the Dog',
        yellow)

    # start screen
    s_text, s_text_rect = create_text(black, yellow, 36, texts[0], game_screen, (1.25, 4))
    game_screen.blit(s_text, s_text_rect)
    pygame.display.flip()

    # loading images
    loaded_dogs = load_images(dogs, game_screen)

    # preparing texts
    dog_s_texts = []
    for i, t in enumerate(texts[1:]):
        text, rect = create_text(black, s_colors[i], 30, t, game_screen, (2, 4))
        dog_t = (text, rect)
        dog_s_texts.append(dog_t)

    # creating iterators to iterate over colors, images, texts in a cycle
    colors_iter = iter(Cycle([color for color in s_colors]))
    dogs_iter = iter(Cycle(loaded_dogs))
    texts_iter = iter(Cycle(dog_s_texts))

    # main game logic
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                color = next(colors_iter)
                game_screen.fill(color)
                if color == yellow:
                    game_screen.blit(s_text, s_text_rect)
                else:
                    game_screen.blit(next(dogs_iter), (game_screen.get_height() // 1.5, game_screen.get_width() // 5))
                    dog_s_text = next(texts_iter)
                    game_screen.blit(dog_s_text[0], dog_s_text[1])
                pygame.display.flip()


if __name__ == "__main__":
    main()

import pygame
from cycle_generator import Cycle


# GAME SETUP STUFF
pygame.init()

# 1) game colors
cyan = (0, 255, 255)
green = (0, 128, 0)
purple = (128, 0, 128)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

s_colors = (cyan, green, purple, yellow)


# 2) game images
dogs = [
    r"C:\Users\user\PycharmProjects\QA_light\lecture_23\images\dog1.webp",
    r"C:\Users\user\PycharmProjects\QA_light\lecture_23\images\dog2.webp",
    r"C:\Users\user\PycharmProjects\QA_light\lecture_23\images\dog3.webp"
]

# 3) game texts
texts = ['Click any mouse button to feed the dog', 'yes, i was a good boy', 'oh!  my!  god!', 'so yummy!']

# 4) creating screen
x = 1000
y = 600
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption('Pygame Mouse Click - Change Color And Feed the Dog')
screen.fill(yellow)

# 5) loading images
loaded_dogs = []
for dog in dogs:
    loaded_dogs.append(pygame.image.load(dog).convert_alpha(screen))


# 5) preparing texts
# ----- start screen
# s_font = pygame.font.Font('LONDON PRESLEY.ttf', 36)
s_font = pygame.font.Font(None, 36)

s_text = s_font.render(texts[0], True, black, yellow)
s_textRect = s_text.get_rect()
s_textRect.center = (x // 2, y // 5)

pygame.display.flip()

# ----- screens with dog
# dog_s_font = pygame.font.Font('LONDON PRESLEY.ttf', 30)
dog_s_font = pygame.font.Font(None, 30)
dog_s_texts = []
for text in texts[1:]:
    t = dog_s_font.render(text, True, white, black)
    rect = t.get_rect()
    rect.center = (x // 4, y // 3)
    dog_t = (t, rect)

    dog_s_texts.append(dog_t)

# - creating iterators to iterate over colors, images, texts in a cycle
colors_iter = iter(Cycle([color for color in s_colors]))
dogs_iter = iter(Cycle(loaded_dogs))
texts_iter = iter(Cycle(dog_s_texts))


# main game logic
def change_color_screen_and_feed_the_dog():
    screen.fill(yellow)
    screen.blit(s_text, s_textRect)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                color = next(colors_iter)
                screen.fill(color)
                if color == yellow:
                    screen.blit(s_text, s_textRect)
                else:
                    screen.blit(next(dogs_iter), (x // 2, y // 5))
                    dog_s_text = next(texts_iter)
                    screen.blit(dog_s_text[0], dog_s_text[1])
                pygame.display.flip()


if __name__ == "__main__":
    change_color_screen_and_feed_the_dog()

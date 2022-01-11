import os
import random
import sys
import pygame
import time
import pygame_menu
from pygame_menu import Theme

pygame.init()
pygame.display.set_caption('Snake')
screen = pygame.display.set_mode((800, 700))
pygame.mixer.music.load("sounds/menu.mp3")
button = pygame.mixer.Sound("sounds/button.mp3")


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class LoseWindow:
    def __init__(self, n):
        s = pygame.mixer.Sound("sounds/game_over_sound.mp3")
        s.play()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = False
            screen.fill((0, 0, 0))
            font1 = pygame.font.SysFont('None', 180)
            font2 = pygame.font.SysFont('None', 100)
            font3 = pygame.font.SysFont('None', 50)
            game_over = font1.render('Game Over', False, (255, 215, 0))
            your_score = font2.render(f'Your score: {n}', False, (255, 255, 255))
            key = font3.render('Нажми на любую кнопку', False, (255, 255, 255))
            screen.blit(game_over, (45, 150))
            screen.blit(your_score, (55, 300))
            screen.blit(key, (200, 650))
            pygame.display.update()


class MiniSnake(pygame.sprite.Sprite):
    image = load_image('snake.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = MiniSnake.image
        self.rect = self.image.get_rect()
        self.rect.x = 720
        self.rect.y = 620


class RestartButton(pygame.sprite.Sprite):
    image = load_image('restart.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = RestartButton.image
        self.rect = self.image.get_rect()
        self.rect.x = 690
        self.rect.y = 0

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            button.play()
            Snake()
            StartWindow()


class MenuButton(pygame.sprite.Sprite):
    image = load_image('menu.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = MenuButton.image
        self.rect = self.image.get_rect()
        self.rect.x = 740
        self.rect.y = 0

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            button.play()
            StartWindow()


class Snake:
    def __init__(self):
        self.x = 400
        self.y = 360
        self.x1 = 0
        self.y1 = 0
        self.le = 1
        self.n = 0
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.apple = pygame.sprite.Sprite(self.all_sprites)
        self.apple.image = load_image('apple.png')
        self.apple.rect = self.apple.image.get_rect()
        self.apple.rect.x = random.randrange(20, 780, 20)
        self.apple.rect.y = random.randrange(60, 680, 20)
        self.game()

    def score(self):
        font = pygame.font.SysFont('None', 48)
        score = font.render(f"Score: {self.n}", False, (255, 215, 0))
        screen.blit(score, (10, 10))

    def background(self):
        screen.fill((124, 252, 0))
        pygame.draw.rect(screen, (32, 232, 14), (0, 0, 800, 40))
        for row in range(31):
            for col in range(38):
                if (row + col) % 2 == 0:
                    color = (219, 239, 255)
                else:
                    color = (255, 255, 255)
                pygame.draw.rect(screen, color, (20 + col * 20, 60 + row * 20, 20, 20))

    def apples(self):
        coin = pygame.mixer.Sound("sounds/coin.mp3")
        if self.x == self.apple.rect.x and self.y == self.apple.rect.y:
            self.apple.rect.x = random.randrange(20, 780, 20)
            self.apple.rect.y = random.randrange(60, 680, 20)
            coin.play()
            self.le += 1
            self.n += 1

    def move(self):
        move = pygame.mixer.Sound("sounds/move.mp3")
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            self.y1 = 1
            self.x1 = 0
            move.play()
        elif key[pygame.K_UP]:
            self.y1 = -1
            self.x1 = 0
            move.play()
        if key[pygame.K_RIGHT]:
            self.x1 = 1
            self.y1 = 0
            move.play()
        elif key[pygame.K_LEFT]:
            self.x1 = -1
            self.y1 = 0
            move.play()

    def collision(self):
        game_over = pygame.mixer.Sound("sounds/game_over.mp3")
        game_over.play()
        time.sleep(2)
        self.running = False
        LoseWindow(self.n)
        pygame.mixer.music.play()

    def game(self):
        snake = [[self.x, self.y]]
        pygame.mixer.music.stop()
        MenuButton(self.all_sprites)
        RestartButton(self.all_sprites)
        MiniSnake(self.all_sprites)
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.mixer.music.play()
                self.move()
                self.all_sprites.update(event)

            self.x += self.x1 * 20
            self.y += self.y1 * 20
            snake.append((self.x, self.y))
            snake = snake[-self.le:]
            self.background()
            self.score()
            [(pygame.draw.rect(screen, (141, 198, 63), (x, y, 20, 20))) for x, y in snake]
            self.apples()
            if self.x >= 780 or self.x < 20 or self.y >= 680 or self.y < 60:
                self.collision()
            if len(snake) > len(set(snake)):
                self.collision()

            clock.tick(5)
            self.all_sprites.draw(screen)
            pygame.display.update()


def start_game():
    button.play()
    Snake()


class StartWindow:
    def __init__(self):
        pygame.mixer.music.play(-1)
        my_theme = Theme(background_color=(124, 252, 0, 200), title_background_color=(0, 128, 0),
                         title_font_shadow=True, widget_padding=20)

        menu = pygame_menu.Menu('Snake', 800, 700, theme=my_theme)
        menu.add.text_input('Введите имя: ', default='Игрок 1')
        menu.add.selector('Выберите уровень сложности: ', [('Лёгкий', 1), ('Средний', 2), ('Тяжёлый', 3)],
                          onchange=self.set_difficulty)
        menu.add.button('Играть', start_game)
        menu.add.button('Выйти', pygame_menu.events.EXIT)

        menu.mainloop(screen)

    def set_difficulty(self, value, difficulty):
        pass


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        StartWindow()


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()

import os
import random
import sys
import pygame
import time
import pygame_menu
from pygame_menu import Theme

pygame.init()
pygame.display.set_caption('Snake')
size = (800, 700)
screen = pygame.display.set_mode(size)
pygame.mixer.music.load("sounds/menu.mp3")
button = pygame.mixer.Sound("sounds/button.mp3")
user_name = ''
game = 0


# загрузка картинок
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


# класс финального окна
class LoseWindow:
    def __init__(self, n):
        s = pygame.mixer.Sound("sounds/game_over_sound.mp3")
        s.play()
        clock = pygame.time.Clock()
        snow = []
        for i in range(200):
            x = random.randrange(0, 800)
            y = random.randrange(0, 700)
            snow.append([x, y])
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = False
            screen.fill((0, 0, 0))
            for i in range(len(snow)):
                pygame.draw.circle(screen, (255, 255, 255), snow[i], 2)
                snow[i][1] += 1
                if snow[i][1] > 700:
                    y = random.randrange(-50, -10)
                    snow[i][1] = y
                    x = random.randrange(0, 800)
                    snow[i][0] = x
            font1 = pygame.font.SysFont('None', 180)
            font2 = pygame.font.SysFont('None', 100)
            font3 = pygame.font.SysFont('None', 50)
            game_over = font1.render('Game Over', False, (255, 215, 0))
            your_score = font2.render(f'Your score: {n}', False, (255, 255, 255))
            key = font3.render('Нажми на любую кнопку', False, (255, 255, 255))
            screen.blit(game_over, (45, 150))
            screen.blit(your_score, (55, 300))
            screen.blit(key, (200, 650))
            clock.tick(60)
            pygame.display.update()


# спрайт маленькой змейки
class MiniSnake(pygame.sprite.Sprite):
    image = load_image('snake.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = MiniSnake.image
        self.rect = self.image.get_rect()
        self.rect.x = 740
        self.rect.y = 640


# спрайт кнопки рестарта
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
            start_game()
            StartWindow()


# спрайт кнопки меню
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
            pygame.mixer.music.play(-1)
            StartWindow()


# спрайт стрелочки для выхода
class ArrowButton(pygame.sprite.Sprite):
    image = load_image('arrow.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ArrowButton.image
        self.rect = self.image.get_rect()
        self.rect.x = -5
        self.rect.y = 0

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            button.play()
            StartWindow()


# отрисовка поля игры
def background():
    screen.fill((124, 252, 0))
    pygame.draw.rect(screen, (32, 232, 14), (0, 0, 800, 40))
    for row in range(31):
        for col in range(38):
            if (row + col) % 2 == 0:
                color = (219, 239, 255)
            else:
                color = (255, 255, 255)
            pygame.draw.rect(screen, color, (20 + col * 20, 60 + row * 20, 20, 20))


# вывод имени и номера игры на игровое поле
def name_game():
    font = pygame.font.SysFont('None', 48)
    name = font.render(f"{user_name.get_value()}", False, (255, 215, 0))
    game1 = font.render(f"Game {game}", False, (255, 215, 0))
    screen.blit(name, (290, 10))
    screen.blit(game1, (550, 10))


# запись счёта, имени и номера игры в файл
def record(n):
    f = open('score.txt', 'a', encoding='utf-8')
    f.write(f'<{user_name.get_value()}> <Game {game}> <Score {n}>\n')
    f.close()


# класс змеи
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

    # вывод счёта на игровом поле
    def score(self):
        font = pygame.font.SysFont('None', 48)
        score = font.render(f"Score: {self.n}", False, (255, 215, 0))
        screen.blit(score, (10, 10))

    # спавн яблока
    def apples(self):
        coin = pygame.mixer.Sound("sounds/coin.mp3")
        if self.x == self.apple.rect.x and self.y == self.apple.rect.y:
            self.apple.rect.x = random.randrange(20, 780, 20)
            self.apple.rect.y = random.randrange(60, 680, 20)
            coin.play()
            self.le += 1
            self.n += 1

    # движение змеи
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

    # столкновения
    def collision(self):
        game_over = pygame.mixer.Sound("sounds/game_over.mp3")
        game_over.play()
        time.sleep(2)
        self.running = False
        record(self.n)
        LoseWindow(self.n)
        pygame.mixer.music.play()

    # игровой цикл
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
                    pygame.mixer.music.play()
                    self.running = False
                self.move()
                self.all_sprites.update(event)

            self.x += self.x1 * 20
            self.y += self.y1 * 20
            snake.append((self.x, self.y))
            snake = snake[-self.le:]
            background()
            name_game()
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


# очистка файла
def clear():
    f = open('score.txt', 'w', encoding='utf-8')
    f.write('')
    button.play()
    f.close()


# запуск класса отрисовки рейтинга
def rating():
    button.play()
    Rating()


# запуск класса змеи
def start_game():
    global game
    button.play()
    game += 1
    Snake()


# класс добавления рейтинга
class Rating:
    def __init__(self):
        self.results()

    def results(self):
        running = True
        all_sprites1 = pygame.sprite.Group()
        ArrowButton(all_sprites1)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                all_sprites1.update(event)

            screen.fill((97, 197, 0))
            self.add_results()
            all_sprites1.draw(screen)
            pygame.display.update()

    def add_results(self):
        f = open('score.txt', 'r', encoding='utf-8')
        lines = f.readlines()
        font = pygame.font.SysFont('None', 48)
        c = font.render('Тут пока ничего нет', False, (255, 255, 255))
        a = 10
        for line in lines:
            a += 30
            score = font.render(line, False, (255, 255, 255))
            screen.blit(score, (10, a))
        if a <= 10:
            screen.blit(c, (250, 100))
        if a > 10:
            screen.blit(c, (-1000, 100))
        f.close()


# класс стартового окна
class StartWindow:
    def __init__(self):
        my_theme = Theme(background_color=(97, 197, 0), title_background_color=(0, 128, 0),
                         title_font_shadow=True, widget_padding=20)

        menu = pygame_menu.Menu('Snake', 800, 700, theme=my_theme)
        global user_name
        user_name = menu.add.text_input('Введите имя: ', default='Игрок 1')
        menu.add.button('Играть', start_game)
        menu.add.button('Рейтинг', rating)
        menu.add.button('Очистить рейтинг', clear)
        menu.add.button('Выйти', pygame_menu.events.EXIT)

        menu.mainloop(screen)


# класс главного цикла
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.mixer.music.play(-1)
        StartWindow()


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()

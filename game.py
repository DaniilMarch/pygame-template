import pygame as pg
from settings import *
from objects import *

"""
Основной класс игры
Состояние игры описывается двумя переменными: running и playing. Если игра
running, то это означает, что приложение работает и игрок будет начинать новую
игру - new() снова и снова. Если игра playing, то в данный момент крутится основной игровой
цикл run() - это происходит внутри new()
"""
class Game:
    """
    Инициализируем pygame, создаем дисплей, название игры, часы и задаем изнчальное
    состояние игры: running = True, загружаем шрифт
    """
    def __init__(self):
        pg.init()
        self.canvas = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Game name")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

    """
    В этом методе реализуется логика новый игры, обнуляем счет, задаем начальные
    положения врагов, игрока и др.
    """
    def new(self):
        self.player = Player()
        self.weapons = []
        self.weapons.append(Weapon(5, 1000, 10, "pistol"))
        self.player.weapon = self.weapons[0]
        self.blocks = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.enemies.add(Enemy())
        self.bullets = pg.sprite.Group()
        self.enemy_spawn_time = 3000
        self.enemy_counter = 1
        pg.time.set_timer(SPAWN_ENEMY, self.enemy_spawn_time)
        self.create_level()
        self.playing = True
        while self.playing:
            self.run()

    """
    Основная функция, в которой реализуется цикл анимации:
    1.Проверяем события
    2.Обновляем положение игровых объектов
    3.Закрашиваем экран цветом заднего фона
    4.Отрисовываем объекты заново
    """
    def run(self):
        self.clock.tick(60)
        self.events()
        self.update()
        self.fill()
        self.draw()

    """
    В этой функции проверям события, проверяем не закрыл ли игрок окно
    """
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == SPAWN_ENEMY:
                if self.enemy_counter % 10 == 0:
                    pg.time.set_timer(SPAWN_ENEMY, 0)
                    self.enemy_spawn_time -= 500
                    pg.time.set_timer(SPAWN_ENEMY, self.enemy_spawn_time)
                self.enemies.add(Enemy())
            if event.type == SHOT_FIRED:
                self.on_shot_fired()

    """
    Обновляем положение игровых объеков
    """
    def update(self):
        self.player.update()
        self.blocks.update()
        self.enemies.update()
        self.bullets.update()
        self.check_collision()

    """
    Закрашиваем экран цветом фона
    """
    def fill(self):
        self.canvas.fill(BG)

    """
    Отрисовываем положение объектов заново
    """
    def draw(self):
        self.player.draw(self.canvas)
        self.blocks.draw(self.canvas)
        self.enemies.draw(self.canvas)
        self.bullets.draw(self.canvas)
        pg.display.flip()

    """
    Вспомогательная функция для отрисовки текста
    """
    def check_collision(self):
        for block in self.blocks:
            for bullet in self.bullets:
                if pg.sprite.collide_rect(bullet, block):
                    bullet.kill()
            if pg.sprite.collide_rect(self.player, block):
                if self.player.rect.top < block.rect.top and\
                self.player.rect.bottom > block.rect.top and\
                block.type == "plat":
                    self.player.rect.bottom = block.rect.top
                    self.player.vel_y = 0
                    self.player.can_jump = True
                elif self.player.rect.bottom > block.rect.bottom and\
                self.player.rect.top < block.rect.bottom and\
                block.type == "plat":
                    self.player.rect.top = block.rect.bottom
                    self.player.vel_y = - self.player.vel_y
                elif self.player.rect.left < block.rect.right and\
                self.player.rect.left > block.rect.left and\
                block.type == "wall":
                    self.player.rect.left = block.rect.right
                elif self.player.rect.right > block.rect.left and\
                self.player.rect.right < block.rect.right and\
                block.type == "wall":
                    self.player.rect.right = block.rect.left
            for enemy in self.enemies:
                if pg.sprite.collide_rect(enemy, block):
                    if enemy.rect.top < block.rect.top and\
                    enemy.rect.bottom > block.rect.top and\
                    block.type == "plat":
                        enemy.rect.bottom = block.rect.top
                        enemy.vel_y = 0
                    elif enemy.rect.bottom > block.rect.bottom and\
                    enemy.rect.top < block.rect.bottom and\
                    block.type == "plat":
                        enemy.rect.top = block.rect.bottom
                        enemy.vel_y = - enemy.vel_y
                    elif enemy.rect.left < block.rect.right and\
                    enemy.rect.left > block.rect.left and\
                    block.type == "wall":
                        enemy.rect.left = block.rect.right
                        enemy.direction*=-1
                    elif enemy.rect.right > block.rect.left and\
                    enemy.rect.right < block.rect.right and\
                    block.type == "wall":
                        enemy.rect.right = block.rect.left
                        enemy.direction*=-1
                for bullet in self.bullets:
                    if pg.sprite.collide_rect(enemy, bullet):
                        enemy.hp -= bullet.damage
                        bullet.kill()
                        if enemy.hp <= 0:
                            enemy.kill()

    def create_level(self):
        self.blocks.add(Block("img\\smallplatform.png", 20, HEIGHT/2, "plat"))
        self.blocks.add(Block("img\\smallplatform.png", 540, HEIGHT/2, "plat"))
        self.blocks.add(Block("img\\bigplatform.png", WIDTH/2-160, HEIGHT/4, "plat"))
        self.blocks.add(Block("img\\bigplatform.png", WIDTH/2-160, HEIGHT*3/4-20, "plat"))
        self.blocks.add(Block("img\\bigplatform.png", 0, 0, "plat"))
        self.blocks.add(Block("img\\bigplatform.png", 400, 0, "plat"))
        self.blocks.add(Block("img\\bigplatform.png", 0, 460, "plat"))
        self.blocks.add(Block("img\\bigplatform.png", 400, 460, "plat"))
        self.blocks.add(Block("img\\leftwall.png", 0, 20, "wall"))
        self.blocks.add(Block("img\\rightwall.png", 700, 20, "wall"))

    def draw_text(self, text, size, text_color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.rendern(text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.canvas.blit(text_surface, text_rect)

    def on_shot_fired(self):
        self.bullets.add(Bullet(self.player.rect.centerx,
                                self.player.rect.centery,
                                self.player.direction,
                                0,
                                self.player.weapon))

game = Game()
while game.running:
    game.new()

pg.quit()

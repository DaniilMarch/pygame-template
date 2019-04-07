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

    """
    Обновляем положение игровых объеков
    """
    def update(self):
        pass

    """
    Закрашиваем экран цветом фона
    """
    def fill(self):
        self.canvas.fill(BG)

    """
    Отрисовываем положение объектов заново
    """
    def draw(self):
        pg.display.flip()

    """
    Вспомогательная функция для отрисовки текста
    """
    def draw_text(self, text, size, text_color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.rendern(text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.canvas.blit(text_surface, text_rect)

game = Game()
while game.running():
    game.new()

pg.quit()

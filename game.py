import pygame as pg
from settings import *
from objects import *

class Game:
    def __init__(self):
        pg.init()
        self.canvas = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Game name")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

    def new(self):
        self.playing = True
        while self.playing:
            self.run()

    def run(self):
        self.events()
        self.update()
        self.fill()
        self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        pass

    def fill(self):
        self.canvas.fill(BG)

    def draw(self):
        pg.display.flip()

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

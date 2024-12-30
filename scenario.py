import pygame as pg
class Scenario:
    def __init__(self, screen, base_path, base_y):
        self.base_path_files = base_path  # base de los archivos
        self.screen = screen  # Contiene información de la pantalla
        self.screen_width, self.screen_height = self.screen.get_size()
        self.base_img_pos_y = base_y
        self.base_img_pos_x = 0
        self.base_img = None
        self.bg_img = None
        self.create()
        self.base_shift=self.solve_calculate_base_shift()


    def create(self):
        self.bg_img = pg.image.load(
            f"{self.base_path_files}assets/sprites/background-day.png").convert()  # background - escenario
        self.base_img = pg.image.load(f"{self.base_path_files}assets/sprites/base.png").convert()  # background terreno

    def solve_calculate_base_shift(self):
        return self.base_img.get_width() - self.bg_img.get_width()

    def update(self):
        self.update_base_img_pos_x()

    def update_base_img_pos_x(self):
        self.base_img_pos_x =-((-self.base_img_pos_x+100) % self.base_shift)

    def draw(self):
        self.screen.blit(self.bg_img, (0, 0))
        self.screen.blit(self.base_img, (self.base_img_pos_x, self.base_img_pos_y))
import pygame as pg
class Score:
    def __init__(self, screen, base_path):
        self.screen = screen
        self.base_path = base_path
        self.font =pg.font.Font(f"{self.base_path}assets/font.ttf",24)
        self.score_text = self.font.render("Score: 0", True, (0, 0, 0))
        self.score_text_rect = self.score_text.get_rect(center=(100, 30))

    def restart(self):
        self.score_text = self.font.render("Score: 0", True, (0, 0, 0))

    def update(self, score):
        self.score_text = self.font.render(f"Score: {score}", True, (0, 0, 0))

    def draw(self):
        self.screen.blit(self.score_text, self.score_text_rect)
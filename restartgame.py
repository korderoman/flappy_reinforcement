import pygame as pg
class RestartGame:
    def __init__(self,screen, base_path):
        self.screen = screen
        self.base_path = base_path
        self.screen_width, self.screen_height = self.screen.get_size()
        self.font = pg.font.Font(f"{self.base_path}assets/font.ttf", 24)
        self.restart_text = self.font.render("Restart", True, (0, 0, 0))
        self.restart_text_rect = self.restart_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2))

    def check_if_click_restart(self, mouse_position):
        return self.restart_text_rect.collidepoint(mouse_position)

    def draw(self, game_over):
        if game_over:
            self.screen.blit(self.restart_text, self.restart_text_rect)

import pygame as pg
from itertools import cycle
from collections import deque
import copy
import random
import sys

from bird import Bird
from config import config
from pipes import Pipe
from q_learning_agent import QLearningAgent
from restartgame import RestartGame
from scenario import Scenario
from score import Score


#from pyvirtualdisplay import Display
class Game:
    def __init__(self, config) -> None:
        self.config = config
        #self.base_path_files = "/content/drive/My Drive/Colab Notebooks/aprendizaje_por reforzamiento/"
        self.base_path_files = ""
        # Características del juego
        self.fps = 30  # cantidad de fotogramas por segundo
        self.screen_width = 288
        self.screen_height = 512
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        self.pipe_gap_size = 100  # distancia entre las tuberías (por donde debe pasar el ave)
        self.state_history = deque(
            maxlen=70)  # Establecemos una cola para los pipes donde la distancia entre ellos sea de 70
        self.images = {}
        self.hit_masks = {}
        self.replay_buffer = []
        self.resume_from=0
        self.game_over = False
        self.initial_len_history=len(self.state_history)
        self.base_y=self.screen_height*0.79
        self.clock = pg.time.Clock()
        self.score_point=0
        # Ejecutamos los métodos iniciales
        self.scenario = Scenario(self.screen,self.base_path_files, self.base_y)
        self.bird=Bird(self.screen,self.base_path_files, self.base_y)
        self.pipe=Pipe(self.screen,self.base_path_files, self.base_y,self.pipe_gap_size)
        self.score=Score(self.screen, self.base_path_files)
        self.qlearning_agent = QLearningAgent(self.config)
        self.restart=RestartGame(self.screen,self.base_path_files)
        self.solve_initial_conditions()
        self.game_loop()

    def solve_initial_conditions(self):
        self.qlearning_agent.solve_check_behaviour_agent()  # determinamos el tipo de comportamiento

    def restart_game(self):
        self.score_point=0
        self.game_over=False
        self.bird.restart()
        self.pipe.restart()

    def draw(self):
        self.scenario.draw()
        self.bird.draw()
        self.pipe.draw()
        self.score.draw()
        self.restart.draw(self.game_over)


    def update(self):
        if not self.game_over:
            self.scenario.update()
            self.bird.update()
            self.pipe.update(self.resume_from,self.initial_len_history)
            self.check_score(self.bird.solve_information_to_crash(),self.pipe.solve_information_to_crash())
            self.score.update(self.score_point)
            self.check_if_is_game_over()


    def check_if_is_game_over(self):
        is_crashed = self.check_if_crash(self.bird.solve_information_to_crash(), self.pipe.solve_information_to_crash())
        self.game_over = is_crashed[0]
        if self.game_over:
            self.qlearning_agent.save_when_is_quit()

    def check_score(self, bird_information, pipes_information):
        player_rect = pg.Rect(bird_information['x'], bird_information['y'],
                              bird_information['w'], bird_information['h'])
        pipe_w = pipes_information["w"]
        pipe_h = pipes_information["h"]
        for l_pipe in pipes_information["lower_pipes"]:
            l_pipe_rect = pg.Rect(l_pipe['x'], l_pipe['y'], pipe_w, pipe_h)
            if l_pipe_rect.right< player_rect.left < l_pipe_rect.right+4:
                self.score_point+=1

    def pixel_collision(self,rect1, rect2, hitmask1, hitmask2):
        """Checks if two objects collide and not just their rects"""
        rect = rect1.clip(rect2)

        if rect.width == 0 or rect.height == 0:
            return False

        x1, y1 = rect.x - rect1.x, rect.y - rect1.y
        x2, y2 = rect.x - rect2.x, rect.y - rect2.y

        for x in range(rect.width):
            for y in range(rect.height):
                if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                    return True
        return False

    def check_if_crash(self, bird_information, pipes_information):
        """Retorna si el ave colisiona con la tierra o una tubería"""
        pi = bird_information['index']
        # si la posición en Y y la altura del ave es mayor que la coordenada de la base
        if bird_information["y"] + bird_information['h'] >= self.base_y - 1:
            return [True, True]
        else:

            player_rect = pg.Rect(bird_information['x'], bird_information['y'],
                                     bird_information['w'], bird_information['h'])
            pipe_w = pipes_information["w"]
            pipe_h = pipes_information["h"]

            for u_pipe, l_pipe in zip(pipes_information["upper_pipes"], pipes_information["lower_pipes"]):
                # upper and lower pipe rects
                u_pipe_rect = pg.Rect(u_pipe['x'], u_pipe['y'], pipe_w, pipe_h)
                l_pipe_rect = pg.Rect(l_pipe['x'], l_pipe['y'], pipe_w, pipe_h)

                # player and upper/lower pipe hitmasks
                p_hit_mask =bird_information['hit_masks'][pi]
                u_hit_mask = pipes_information['hit_masks'][0]
                l_hit_mask = pipes_information['hit_masks'][1]

                # if bird collided with upipe or lpipe
                u_collide = self.pixel_collision(player_rect, u_pipe_rect, p_hit_mask, u_hit_mask)
                l_collide = self.pixel_collision(player_rect, l_pipe_rect, p_hit_mask, l_hit_mask)

                if u_collide or l_collide:
                    return [True, False]

        return [False, False]

    def check_events(self):
        for event in pg.event.get():
            #Se configura el evento de salida
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.qlearning_agent.save_when_is_quit()
                pg.quit()
                sys.exit()
            if event.type== pg.KEYDOWN and event.key == pg.K_SPACE:
                self.bird.flap_by_space_event()
            if event.type==pg.MOUSEBUTTONUP and self.game_over:
                 if self.restart.check_if_click_restart(pg.mouse.get_pos()):
                     self.restart_game()

        #******* El agente evalúa si realiza una acción de aleteo
        should_be_act =self.qlearning_agent.should_be_act(self.bird.pos_x, self.bird.pos_y,self.bird.vel_y,self.pipe.pipe_down_positions)
        if should_be_act and not self.config['is_manual'] :
            self.bird.flap_by_space_event()

    def game_loop(self):
        while True:
            self.check_events()
            if self.config['show_game']:
                self.draw()
                self.update()
                pg.display.update()
                self.clock.tick(self.fps)

pg.init()
game=Game(config)
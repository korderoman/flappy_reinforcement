import random

import pygame as pg

class Pipe:
    def __init__(self,screen, base_path, base_y, pipe_gap_size):
        self.screen = screen
        self.base_y = base_y
        self.pipe_gap_size = pipe_gap_size
        self.screen_width, self.screen_height = self.screen.get_size()
        self.base_path = base_path
        self.pipe_up,self.pipe_down=self.create()
        self.pipe_up_positions, self.pipe_down_positions=self.get_positions()
        #Datos compartidos en todo el juego
        self.vel_x=-4

    def create(self):
        pipe_asset_path=f"{self.base_path}assets/sprites/pipe-green.png"
        pipe_up=pg.transform.rotate(pg.image.load(pipe_asset_path).convert_alpha(), 180)
        pipe_down=pg.image.load(pipe_asset_path).convert_alpha()
        return pipe_up, pipe_down

    def get_random_pipe(self):
        """Retorna un punto random del pipe y su gap, siendo el gap la distancia entre los pipes"""
        gap_y = random.randrange(0, int(self.base_y * 0.6 - self.pipe_gap_size))
        gap_y += int(self.base_y * 0.2)
        pipe_height = self.pipe_up.get_height()
        pipe_x = self.screen_width + 10

        return [
            {'x': pipe_x, 'y': gap_y - pipe_height},  # upper pipe
            {'x': pipe_x, 'y': gap_y + self.pipe_gap_size},  # lower pipe
        ]
    def get_positions(self):
        pipe_1=self.get_random_pipe()
        pipe_2=self.get_random_pipe()
        upper_pipes = [
            {'x': self.screen_width + 200, 'y': pipe_1[0]['y']},
            {'x': self.screen_width + 200 + (self.screen_width / 2), 'y': pipe_2[0]['y']},
        ]


        lower_pipes = [
            {'x': self.screen_width + 200, 'y': pipe_1[1]['y']},
            {'x': self.screen_width + 200 + (self.screen_width / 2), 'y': pipe_2[1]['y']},
        ]

        return upper_pipes, lower_pipes


    def draw(self):
        for u_pipe, l_pipe in zip(self.pipe_up_positions,self.pipe_down_positions):
            self.screen.blit(self.pipe_up,(u_pipe['x'], u_pipe['y']))
            self.screen.blit(self.pipe_down, (l_pipe['x'], l_pipe['y']))

    def update(self, resume,initial_len_history):
        self.update_pipes_position(resume,initial_len_history)
        self.add_pipe_when_first_pipe_touch_left_screen()
        self.remove_first_pipe_when_is_out_of_screen()

    def update_pipes_position(self, resume,initial_len_history):
        if resume>=initial_len_history:
            for u_pipe, l_pipe in zip(self.pipe_up_positions,self.pipe_down_positions):
                u_pipe['x'] += self.vel_x
                l_pipe['x'] += self.vel_x
    def add_pipe_when_first_pipe_touch_left_screen(self):
        if 0 < self.pipe_down_positions[0]['x']< 5:
            new_pipe=self.get_random_pipe()
            self.pipe_up_positions.append(new_pipe[0])
            self.pipe_down_positions.append(new_pipe[1])

    def remove_first_pipe_when_is_out_of_screen(self):
        if self.pipe_down_positions[0]['x'] < -self.pipe_down.get_width():
            self.pipe_up_positions.pop(0)
            self.pipe_down_positions.pop(0)

    def solve_information_to_crash(self):
        return {
            "w":self.pipe_up.get_width(),
            "h":self.pipe_up.get_height(),
            "upper_pipes": self.pipe_up_positions,
            "lower_pipes": self.pipe_down_positions,
            "hit_masks": self.get_hit_masks(),
        }

    def get_hit_mask(self, image):
        """Returns a hitmask using an image's alpha."""
        mask = []
        for x in range(image.get_width()):
            mask.append([])
            for y in range(image.get_height()):
                mask[x].append(bool(image.get_at((x, y))[3]))
        return mask

    def get_hit_masks(self):
        pipe_list=[self.pipe_up,self.pipe_down]
        return [self.get_hit_mask(x) for x in pipe_list]
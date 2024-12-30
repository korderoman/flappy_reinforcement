from itertools import cycle

import pygame as pg
class Bird:
    def __init__(self, screen, base_path, base_y):
        self.screen = screen
        self.base_path = base_path
        self.base_y = base_y
        self.image_list=self.create()
        self.image_index=0
        self.screen_width, self.screen_height = self.screen.get_size()
        self.image=self.image_list[self.image_index]
        self.player_index_gen=cycle([0,1,2,1])
        self.loop_iter=0
        self.pos_x=int(self.screen_width * 0.2)
        self.pos_y=self.calculate_bird_pos_y()
        #características que serán usadas en el juego
        self.vel_y=-9
        self.flap_acc=-9 #velocidad del aleteo
        self.flapped=False #cambia a verdadero cuando aletea
        self.max_vel_y=10 # máxima velocidad de descenso
        self.min_vel_y=-8 # Velocidad mínima de ascenso
        self.acc_y=1 #velocidad de aceleración en descenso

    def calculate_bird_pos_y(self):
        return int((self.screen_height-self.image_list[0].get_height())/2)
    def create(self):
        bird_assets = [f"{self.base_path}assets/sprites/bluebird-downflap.png", f"{self.base_path}assets/sprites/bluebird-midflap.png", f"{self.base_path}assets/sprites/bluebird-upflap.png"]
        return [pg.image.load(x).convert_alpha() for x in bird_assets]

    def flap_by_space_event(self):
        """
        Realiza un aleteo cada vez que se da un evento de espaciado
        :return:
        """
        if self.pos_y> -2*self.image.get_height():
            self.vel_y=self.flap_acc
            self.flapped=True


    def draw(self):
        self.screen.blit(self.image, (self.pos_x, self.pos_y))

    def update(self):
        self.play_animation()
        self.apply_gravity()
        self.check_if_flapped()

    def play_animation(self):
        if(self.loop_iter +1) %3==0: #cada múltiplo de 3 se realiza un cambio de imagen
            self.image_index=next(self.player_index_gen) #pasamos al siguiente elemento del iterado
            self.image=self.image_list[self.image_index] # redefinimos la imagen
        self.loop_iter=(self.loop_iter+1)%30 # en caso de no ser múltiplo seguimos recorriendo

    def solve_information_to_crash(self):
        return {
            "x":self.pos_x,
            "y":self.pos_y,
            "w":self.image.get_width(),
            "h":self.image.get_height(),
            "hit_masks":self.get_hit_masks(),
            "index":self.image_index,
        }
    def apply_gravity(self):
        """
        Evalúa la velocidad en Y del ave y establece su posición en Y
        """
        if self.vel_y<self.max_vel_y and not self.flapped:
            self.vel_y+=self.acc_y
        self.pos_y+=min(self.vel_y,self.base_y-self.pos_y-self.image.get_height())

    def get_hit_mask(self, image):
        """Retorna la mascara de golpe usando un rectángulo."""
        mask = []
        for x in range(image.get_width()):
            mask.append([])
            for y in range(image.get_height()):
                mask[x].append(bool(image.get_at((x, y))[3]))
        return mask

    def get_hit_masks(self):
        return [self.get_hit_mask(x) for x in self.image_list]


    def check_if_flapped(self):
        """
        Examina si el ave aleteó
        :return:
        """
        if self.flapped:
            self.flapped = False
    def restart(self):
        self.image_list = self.create()
        self.image_index = 0
        self.screen_width, self.screen_height = self.screen.get_size()
        self.image = self.image_list[self.image_index]
        self.player_index_gen = cycle([0, 1, 2, 1])
        self.loop_iter = 0
        self.pos_x = int(self.screen_width * 0.2)
        self.pos_y = self.calculate_bird_pos_y()
        # características que serán usadas en el juego
        self.vel_y = -9
        self.flap_acc = -9  # velocidad del aleteo
        self.flapped = False  # cambia a verdadero cuando aletea
        self.max_vel_y = 10  # máxima velocidad de descenso
        self.min_vel_y = -8  # Velocidad mínima de ascenso
        self.acc_y = 1  # velocidad de aceleración en descenso


import pygame
from src.player import Player

class Laserbeam(pygame.sprite.Sprite):
    def __init__(self, width = 5, height = 40, pos_x = 275, pos_y = 500, laserbeam_color = "lime"):
        '''
        Initializes data for class object
        args: (integer) pos_x, pos_y, width and height of laserbeam
        '''
        super().__init__()
        
        self.player = Player()
        self.surface_obj = pygame.Surface((width,height))
        self.surface_obj.fill(laserbeam_color)
        self.rect = self.surface_obj.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
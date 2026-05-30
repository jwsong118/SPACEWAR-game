import pygame

class Abilitybox(pygame.sprite.Sprite):
    
    def __init__(self, pos_x=275, pos_y=0, width = 30, height = 30):
        '''
        Initializes data for class object
        args: (integer) pos_x, pos_y, width and height of abilitybox
        '''
        super().__init__()
        
        self.image_path = "assets/ability_shoot.png"
        self.original_image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.original_image, (width,height))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

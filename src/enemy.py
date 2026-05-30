import pygame

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, pos_x=275, pos_y=0, width=30, height=90, image_path = "assets/enemyship.png"):
        '''
        Initializes data for class object
        args: (integer, png) pos_x, pos_y, width and height of enemyship, image of enemyship
        '''
        super().__init__()
        
        self.original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.original_image, (width,height))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = 10
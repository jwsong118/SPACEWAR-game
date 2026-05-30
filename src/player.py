import pygame

class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos_x=275, pos_y=520, width = 50, height = 80, image_path = "assets/starship.png"):
        '''
        Initializes data for class object
        args: (integer,png) pos_x, pos_y, width and height of playership, image of playership
        '''
        super().__init__()
        
        self.original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.original_image, (width,height))
        self.rect = self.image.get_rect()
        self.colliderect = pygame.rect.Rect((self.rect.x + 7 ,self.rect.y),(36,80))
        self.rect.x = pos_x 
        self.rect.y = pos_y
        self.speed = 5
    
        
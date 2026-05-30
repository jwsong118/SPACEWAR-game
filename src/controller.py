import pygame
import random
import math
from pygame import mixer
from src.player import Player
from src.enemy import Enemy
from src.laserbeam import Laserbeam
from src.abilitybox import Abilitybox

class Controller:
  
  def __init__(self):
    '''
    initializes values for the whole class object
    '''
    #setup pygame data
    pygame.init()
    self.SCREEN_WIDTH = 600
    self.SCREEN_HEIGHT = 700
    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
    self.clock = pygame.time.Clock()
    self.player = Player()
    self.enemy = Enemy()
    self.laserbeam = Laserbeam()
    self.abilitybox = Abilitybox()
    self.enemies = pygame.sprite.Group()
    self.laserbeams = pygame.sprite.Group()
    self.abilityboxes = pygame.sprite.Group()
    self.STATE = "MENU"
    self.background_image = pygame.image.load("assets/background.jpg")
    self.image = pygame.transform.scale(self.background_image, (self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
    self.rect = self.image.get_rect()
    mixer.music.load("assets/posterity.mp3")
    mixer.music.play(-1)
    
  def mainloop(self):
    '''
    controlls the whole menuloop,gameloop,gamoverloop
    '''
  
    while True:
      
      #select state loop
      if self.STATE == "MENU":
        self.menuloop()
      if self.STATE == "GAME":
        self.gameloop()
      if self.STATE == "GAMEOVER":
        self.gameoverloop()
  
  def menuloop(self):
    '''
    displays the menu
    '''
    
    info_image = pygame.image.load("assets/info.png")
    back_image = pygame.image.load("assets/back.png")
    self.info_image_x = 0
    self.info_image_y = 0
    self.menu_info_image = pygame.transform.scale(info_image, (30,30))
    self.menu_info_image_rect = self.menu_info_image.get_rect()
    self.menu_back_image = pygame.transform.scale(back_image,(50,30))
    self.menu_back_image_rect =self.menu_back_image.get_rect()
    display_info = False
    
    while self.STATE == "MENU":
      
      #event loop
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            gamestart_sound = mixer.Sound("assets/gamestart_sound.wav")
            gamestart_sound.play()
            self.STATE = "GAME"
        if event.type == pygame.MOUSEBUTTONDOWN:
          if self.menu_info_image_rect.collidepoint(event.pos):
            gamestart_sound = mixer.Sound("assets/gamestart_sound.wav")
            gamestart_sound.play()
            display_info = True
          if self.menu_back_image_rect.collidepoint(event.pos):
            gamestart_sound = mixer.Sound("assets/gamestart_sound.wav")
            gamestart_sound.play()
            display_info = False
          
      #update data
      self.screen.fill((0,0,0))
      if display_info:
        self.font = pygame.font.Font("assets/Inversionz.ttf", 30)
        self.rules_of_game_0 = self.font.render("ABOUT GAME", True, "white")
        self.rules_of_game_1 = self.font.render("# avoid the killerships", True, "white")
        self.rules_of_game_2 = self.font.render("# get the abilitybox", True, "white")
        self.rules_of_game_3 = self.font.render("# the abilities are", True, "white")
        self.rules_of_game_4 = self.font.render("shooting, speed, shield", True, "white")
        self.rules_of_game_5 = self.font.render("# max 2 abilities", True, "white")
        self.rules_of_game_6 = self.font.render("# if 2 same abilities,", True, "white")
        self.rules_of_game_7 = self.font.render("your ability will get upgraded", True, "white")
        self.rules_of_game_8 = self.font.render("HOW TO PLAY", True, "white")
        self.rules_of_game_9 = self.font.render("left,right,up,down keys to move", True, "white")
        self.rules_of_game_10= self.font.render("press 's' to shoot", True, "white")
        
        self.screen.blit( self.rules_of_game_0, (208,50))
        self.screen.blit( self.rules_of_game_1, (80,100))
        self.screen.blit( self.rules_of_game_2, (110,150))
        self.screen.blit( self.rules_of_game_3, (120,200))
        self.screen.blit( self.rules_of_game_4, (80,250))
        self.screen.blit( self.rules_of_game_5, (130,300))
        self.screen.blit( self.rules_of_game_6, (90,350))
        self.screen.blit( self.rules_of_game_7, (12,400))
        self.screen.blit( self.rules_of_game_8, (200,500))
        self.screen.blit( self.rules_of_game_9, (5,550))
        self.screen.blit( self.rules_of_game_10, (130,600))
        self.screen.blit(self.menu_back_image,(550,0))
        
            
      else:    
        self.font = pygame.font.Font("assets/Inversionz.ttf", 100)
        self.game_name = self.font.render("SPACEWAR", True, "white")
        self.font = pygame.font.Font("assets/Inversionz.ttf", 40)
        self.starting_text =self.font.render("press [space] to play", True, "white")
        
        self.screen.blit(self.starting_text, (30,550))
        self.screen.blit(self.game_name, (50,180))
        self.screen.blit(self.menu_info_image,(self.info_image_x,self.info_image_y))
      
      self.menu_info_image_rect.topleft = (self.info_image_x, self.info_image_y)
      self.menu_back_image_rect.topleft = (550, 0)
      #redraw
      pygame.display.flip()
      
  def gameloop(self):
    '''
    displays the game screen
    '''
    
    self.adding_enemy_2 = []
    self.adding_enemy_3 = []
    self.adding_enemy_4 = []
    self.number_of_abilitybox = []
    self.shield_list = []
    self.speed_list = []
    self.shoot_list = []
    self.player.speed = 5
    # Fill the screen with background image
    self.screen.blit(self.image, self.rect)
    self.key_left_pressed = False
    self.key_right_pressed = False
    self.key_up_pressed = False
    self.key_down_pressed = False
    self.key_s_pressed = False
    self.check = False
    self.shootinglaser = False
    abilitybox_changed = False
    self.time_in_the_menuloop = pygame.time.get_ticks() 
    self.enemy_speed = 12
    first_laserbeam_width = 5
    first_laserbeam_height = 40
    player_width = 50
    player_height = 80
    laserbeam_speed = 80
    abilitybox_speed = 3
    enemy_width = 30
    enemy_height = 90
    abilitybox_width = 30
    
    for n in range(2):
      self.enemies.add(Enemy(random.randint(0,550),-50))
    tiles = math.ceil(700/600) + 2
    scroll = 0
    
    while self.STATE == "GAME":
        
        self.time_in_the_gameloop = pygame.time.get_ticks() 

        #event loop
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            pygame.quit()
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                self.key_left_pressed = True
              if event.key == pygame.K_RIGHT:
                self.key_right_pressed = True
              if event.key == pygame.K_UP:
                self.key_up_pressed = True
              if event.key == pygame.K_DOWN:
                self.key_down_pressed = True
              if event.key == pygame.K_s and not self.check and self.shootinglaser == True :
                lasershot_sound = mixer.Sound("assets/lasershot_sound.wav")
                lasershot_sound.play()
                self.laserbeam.rect.x = self.player.rect.x + player_width/2 - first_laserbeam_width//2
                self.laserbeam.rect.y = self.player.rect.y + first_laserbeam_height
                self.check = True
                if self.shoot_list == [1,1]:
                  self.laserbeam.surface_obj =pygame.Surface((first_laserbeam_width*4,first_laserbeam_height))
                  self.laserbeam.surface_obj.fill("lime") 
                  self.laserbeam.rect = self.laserbeam.surface_obj.get_rect()
                  self.laserbeam.rect.x = self.player.rect.x + player_width/2 - first_laserbeam_width*2
                  self.laserbeam.rect.y = self.player.rect.y + first_laserbeam_height
                  
                
          if event.type == pygame.KEYUP:
              if event.key == pygame.K_LEFT:
                self.key_left_pressed = False
              if event.key == pygame.K_RIGHT:
                self.key_right_pressed = False
              if event.key == pygame.K_UP:
                self.key_up_pressed = False
              if event.key == pygame.K_DOWN:
                self.key_down_pressed = False
              
        
        if self.key_left_pressed:
          self.player.rect.x -= self.player.speed
          self.player.rect.x = max(self.player.rect.x,0)
        if self.key_right_pressed:
          self.player.rect.x += self.player.speed
          self.player.rect.x = min(self.player.rect.x,self.SCREEN_WIDTH - player_width)
        if self.key_up_pressed:
          self.player.rect.y -= self.player.speed
          self.player.rect.y = max(self.player.rect.y,600 - player_height*2)
        if self.key_down_pressed:
          self.player.rect.y += self.player.speed
          self.player.rect.y = min(self.player.rect.y,self.SCREEN_HEIGHT - player_height)
          
        #Fill the screen with background image
        self.image = pygame.transform.scale(self.background_image, (self.SCREEN_WIDTH,self.SCREEN_WIDTH))
        for i in range(0, tiles):
          self.screen.blit(self.image, (0,self.SCREEN_HEIGHT-self.SCREEN_WIDTH + (-i)*self.SCREEN_WIDTH + scroll))
        
        scroll += 1
        
        if abs(scroll) > self.SCREEN_WIDTH :
          scroll = 0
          
          
        #Shooting laserbeams
        if self.check and self.shoot_list == [1]: 
          self.laserbeam.rect.y -= laserbeam_speed
          self.screen.blit(self.laserbeam.surface_obj, self.laserbeam.rect)
          
          if self.laserbeam.rect.y <= 0 :
            
            self.laserbeam.kill()
            self.check = False
          
          for enemy in self.enemies:
            if pygame.sprite.collide_rect(self.laserbeam, enemy):
              explosion_sound = mixer.Sound("assets/explosion_sound.wav")
              explosion_sound.play()
              self.laserbeam.kill()
              self.check = False
              enemy.kill() 
              self.enemies.add(Enemy(random.randint(0,self.SCREEN_WIDTH - enemy_width), -enemy_height))
          
          for laserbeam in self.laserbeams:
            laserbeam.kill()
        
        if self.check and self.shoot_list == [1,1]: 
          
          mask_surface = pygame.Surface((first_laserbeam_width*2, first_laserbeam_height))
          mask_surface.fill("black")
          self.laserbeam.rect.y -= laserbeam_speed
          self.screen.blit(self.laserbeam.surface_obj, self.laserbeam.rect)
          self.screen.blit(mask_surface, (self.laserbeam.rect.x + first_laserbeam_width, self.laserbeam.rect.y))
          
          if self.laserbeam.rect.y <= 0 :
            
            self.laserbeam.kill()
            self.check = False
          
          for enemy in self.enemies:
            if pygame.sprite.collide_rect(self.laserbeam, enemy):
              explosion_sound = mixer.Sound("assets/explosion_sound.wav")
              explosion_sound.play()
              self.laserbeam.kill()
              self.check = False
              enemy.kill() 
              self.enemies.add(Enemy(random.randint(0,self.SCREEN_WIDTH - enemy_width ), -enemy_height))
          
          for laserbeam in self.laserbeams:
            laserbeam.kill()
        
        #update data for enemies
        for enemy in self.enemies:
          enemy.rect.y += self.enemy_speed
          if self.SCREEN_WIDTH < enemy.rect.y <= self.SCREEN_WIDTH + 13:
            for n in range(1):
              self.enemies.add(Enemy(random.randint(0,self.SCREEN_WIDTH - enemy_width), -enemy_height))
          if enemy.rect.y >= self.SCREEN_HEIGHT + enemy_height :
            enemy.kill()

        if 20000 < self.time_in_the_gameloop - self.time_in_the_menuloop <= 40000 and self.adding_enemy_2==[] :
          for n in range(2):
            self.enemies.add(Enemy(random.randint(0,self.SCREEN_WIDTH - enemy_width), -enemy_height))
          self.adding_enemy_2.append(1)
          self.enemy_speed = 12
          self.abilityboxes.add(Abilitybox(random.randint(0,self.SCREEN_WIDTH - abilitybox_width),-50))
        
        if 50000 < self.time_in_the_gameloop - self.time_in_the_menuloop <= 70000 and self.adding_enemy_3==[] :
          for n in range(2):
            self.enemies.add(Enemy(random.randint(0,self.SCREEN_WIDTH - enemy_width), -enemy_height))
          self.adding_enemy_3.append(1)
          self.enemy_speed = 12
          self.abilityboxes.add(Abilitybox(random.randint(0,self.SCREEN_WIDTH - abilitybox_width),-50))
          
        if 120000 < self.time_in_the_gameloop - self.time_in_the_menuloop <= 130000 and self.adding_enemy_4==[] :
          for n in range(2):
            self.enemies.add(Enemy(random.randint(0,self.SCREEN_WIDTH - enemy_width), -enemy_height))
          self.adding_enemy_4.append(1)
          self.enemy_speed = 13
        
        for enemy in self.enemies:
          if pygame.sprite.collide_rect(self.player, enemy) and self.shield_list ==[] :
              gameover_sound = mixer.Sound("assets/gameover_sound.wav")
              gameover_sound.play()
              self.player.kill()
              for enemy in self.enemies:
                enemy.kill()
              for abilitybox in self.abilityboxes:
                abilitybox.kill()
              scoredata = open("etc/highestscore.txt")
              self.highestscore = scoredata.read()
              if (self.time_in_the_gameloop - self.time_in_the_menuloop)/1000 > int(self.highestscore):
                updatedata = open("etc/highestscore.txt", "w")
                updatedata.write(f"{(self.time_in_the_gameloop - self.time_in_the_menuloop)//1000+1}")
                updatedata.close()
                scoredata = open("etc/highestscore.txt")
                self.highestscore = scoredata.read()
              self.STATE = "GAMEOVER"  
              
        for enemy in self.enemies:
          if pygame.sprite.collide_rect(self.player, enemy) and self.shield_list ==[1]:
            self.shield_list.remove(1)
            gameover_sound = mixer.Sound("assets/gameover_sound.wav")
            gameover_sound.play()
            enemy.kill()
            self.player.kill()
            self.player.image = pygame.transform.scale( pygame.image.load("assets/starship.png"), (player_width,player_height))
            self.player.add()
            for n in range(1):
              self.enemies.add(Enemy(random.randint(0,self.SCREEN_WIDTH - enemy_width),0))
              
        for enemy in self.enemies:
          if pygame.sprite.collide_rect(self.player, enemy) and self.shield_list ==[1,1]:
            self.shield_list.remove(1)
            gameover_sound = mixer.Sound("assets/gameover_sound.wav")
            gameover_sound.play()
            enemy.kill()
            self.player.kill()
            self.player.image = pygame.transform.scale( pygame.image.load("assets/starship_shielded.png"), (player_width,player_height))
            self.player.add()
            for n in range(1):
              self.enemies.add(Enemy(random.randint(0,self.SCREEN_WIDTH - enemy_width),0))
        
        # Update data for abilitybox
        for abilitybox in self.abilityboxes:
            
            abilitybox.rect.y = abilitybox.rect.y + abilitybox_speed
            
            if not abilitybox_changed:
              abilitybox.image_path = random.choice([ "assets/ability_shoot.png", "assets/ability_shield.png" ])
              original_image = pygame.image.load(abilitybox.image_path)
              abilitybox.image = pygame.transform.scale(original_image, (abilitybox_width,abilitybox_width))
              abilitybox_changed = True
            
            if pygame.sprite.collide_rect(self.player, abilitybox) and abilitybox.image_path == "assets/ability_shoot.png":
              self.shoot_list.append(1)
              if self.shoot_list == [1]:
                shield_sound = mixer.Sound("assets/shield_sound.wav")
                shield_sound.play()
                self.shootinglaser = True
                abilitybox.kill()
                abilitybox_changed = False
              if self.shoot_list == [1,1]:
                shield_sound = mixer.Sound("assets/shield_sound.wav")
                shield_sound.play()
                self.shootinglaser = True
                abilitybox.kill()
                abilitybox_changed = False
                
            if pygame.sprite.collide_rect(self.player, abilitybox) and abilitybox.image_path == "assets/ability_speed.png":
              self.speed_list.append(1)
              if self.speed_list == [1]:
                shield_sound = mixer.Sound("assets/shield_sound.wav")
                shield_sound.play()
                self.player.speed = 6
                abilitybox.kill()
                abilitybox_changed = False
              if self.speed_list == [1,1]:
                shield_sound = mixer.Sound("assets/shield_sound.wav")
                shield_sound.play()
                self.player.speed = 7
                abilitybox.kill()
                abilitybox_changed = False
                
            if pygame.sprite.collide_rect(self.player, abilitybox) and abilitybox.image_path == "assets/ability_shield.png":
              self.shield_list.append(1)
              if self.shield_list == [1]:
                shield_sound = mixer.Sound("assets/shield_sound.wav")
                shield_sound.play()
                shielded_image = pygame.image.load("assets/starship_shielded.png")
                self.player.image = pygame.transform.scale(shielded_image, (player_width,player_height))
              if self.shield_list == [1,1]:
                shield_sound = mixer.Sound("assets/shield_sound.wav")
                shield_sound.play()
                shielded_image = pygame.image.load("assets/starship_shielded_2.png")
                self.player.image = pygame.transform.scale(shielded_image, (player_width,player_height))
              
              abilitybox.kill()
              
              abilitybox_changed = False
            
            if abilitybox.rect.y >= 750:
              abilitybox.kill()
              
        #Fill the screen with player
        self.screen.blit(self.player.image, self.player.rect) 
        
        #Fill the screen with abilitybox
        for abilitybox in self.abilityboxes:
          self.screen.blit(abilitybox.image,abilitybox.rect)
        
        #Fill the screen with enemies
        for enemy in self.enemies:
          self.screen.blit(enemy.image, enemy.rect)
          
        pygame.display.flip() #redraw
        self.clock.tick(30)  # Set the frame rate to 30 frames per second

    
  def gameoverloop(self):
    '''
    displays the gameoverscreen
    '''
    
    while self.STATE == "GAMEOVER" :
      
      #event loop
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            gamestart_sound = mixer.Sound("assets/gamestart_sound.wav")
            gamestart_sound.play()
            self.STATE = "MENU"
          
      pygame.font.init()    
      self.font = pygame.font.Font("assets/Inversionz.ttf", 40)
      self.screen.fill((0,0,0))
        
      
      #update data
      if (self.time_in_the_gameloop - self.time_in_the_menuloop)/1000 <= 45:
        self.highest = f"GOAT : {self.highestscore} SEC"
        self.goat = self.font.render(self.highest, True, "white")
        self.comment = "try better next time"
        self.end_comment = self.font.render(self.comment, True, "white")
        self.score = f"your score : {(self.time_in_the_gameloop - self.time_in_the_menuloop)//1000+1} sec"
        self.end_score = self.font.render(self.score, True, "white")
        self.restart = "PRESS [SPACE] FOR MENU"
        self.end_restart = self.font.render(self.restart, True, "white")
        self.screen.blit(self.goat, (120, 100))
        self.screen.blit(self.end_score, (50,250))
        self.screen.blit(self.end_comment, (40,350))
        self.screen.blit(self.end_restart, (30,550))
        pygame.display.flip()
      
      if 45 <(self.time_in_the_gameloop - self.time_in_the_menuloop)/1000 <= 90:
        self.highest = f"GOAT : {self.highestscore} SEC"
        self.goat = self.font.render(self.highest, True, "white")
        self.comment = "semi pro"
        self.end_comment = self.font.render(self.comment, True, "white")
        self.score = f"your score : {(self.time_in_the_gameloop - self.time_in_the_menuloop)//1000+1} sec"
        self.end_score = self.font.render(self.score, True, "white")
        self.restart = "PRESS [SPACE] FOR MENU"
        self.end_restart = self.font.render(self.restart, True, "white")
        self.screen.blit(self.goat, (120, 100))
        self.screen.blit(self.end_score, (50,250))
        self.screen.blit(self.end_comment, (190,350))
        self.screen.blit(self.end_restart, (30,550))
        pygame.display.flip()
      
      if (self.time_in_the_gameloop - self.time_in_the_menuloop)/1000 > 90:
        self.highest = f"GOAT : {self.highestscore} SEC"
        self.goat = self.font.render(self.highest, True, "white")
        self.comment = "pro level"
        self.end_comment = self.font.render(self.comment, True, "white")
        self.score = f"your score : {(self.time_in_the_gameloop - self.time_in_the_menuloop)//1000+1} sec"
        self.end_score = self.font.render(self.score, True, "white")
        self.restart = "PRESS [SPACE] FOR MENU"
        self.end_restart = self.font.render(self.restart, True, "white")
        self.screen.blit(self.goat, (120, 100))
        self.screen.blit(self.end_score, (50,250))
        self.screen.blit(self.end_comment, (180,350))
        self.screen.blit(self.end_restart, (30,550))
        
        #redraw
        pygame.display.flip()
      
      

    

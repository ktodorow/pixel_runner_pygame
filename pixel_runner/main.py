import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    __player_x_pos = 50 
    __player_y_pos = 300
    
    def __init__(self, scale_factor = 1):
        super().__init__()

        player_walk_1 = pygame.image.load(fr"graphics\player\player2_walk1.png").convert_alpha()
        player_walk_2 = pygame.image.load(fr"graphics\player\player2_walk2.png").convert_alpha()
        self.player_jump = pygame.image.load(fr"graphics\player\player2_jump.png").convert_alpha()

        # Sunny-Bunny player
        # player_walk_1 = pygame.image.load(fr"graphics\player\bunny_player\run\_0000_Layer-1.png").convert_alpha()
        # player_walk_2 = pygame.image.load(fr"graphics\player\bunny_player\run\_0001_Layer-2.png").convert_alpha()
        # self.player_jump = pygame.image.load(fr"graphics\player\bunny_player\jump\_0000_Layer-1.png").convert_alpha()

        # # apply scaling
        # player_walk_1 = pygame.transform.scale(player_walk_1, (int(player_walk_1.get_width() * scale_factor), int(player_walk_1.get_height() * scale_factor)))
        # player_walk_2 = pygame.transform.scale(player_walk_2, (int(player_walk_2.get_width() * scale_factor), int(player_walk_2.get_height() * scale_factor)))
        # self.player_jump = pygame.transform.scale(self.player_jump, (int(self.player_jump.get_width() * scale_factor), int(self.player_jump.get_height() * scale_factor)))

        self.player_walk_anim = [player_walk_1, player_walk_2]
        self.player_index = 0

        self.image = self.player_walk_anim[self.player_index]
        self.rect = self.image.get_rect(midbottom = (self.__player_x_pos, self.__player_y_pos))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: 
            self.rect.bottom = 300
            self.gravity = 0

    def player_animation(self):
        if self.rect.bottom < 300: self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk_anim): self.player_index = 0
            self.image = self.player_walk_anim[int(self.player_index)] 

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animation()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type, score):
        super().__init__()
        
        match (type):
            case "fly":
                _y_pos = 212
                fly_frame_1 = pygame.image.load(fr"graphics\fly\fly1.png").convert_alpha()
                fly_frame_2 = pygame.image.load(fr"graphics\fly\fly2.png").convert_alpha()
                self.frames = [fly_frame_1, fly_frame_2]
            case "snail":
                _y_pos = 300 
                snail_frame_1 = pygame.image.load(fr"graphics\snail\snail1.png").convert_alpha()
                snail_frame_2 = pygame.image.load(fr"graphics\snail\snail2.png").convert_alpha()
                self.frames = [snail_frame_1, snail_frame_2]
            case _:
                raise Exception("Err(OBSTACLE_NOT_FOUND)")
        self.speed = 5
        self.type_index = 0
        self.image = self.frames[self.type_index]
        self.rect = self.image.get_rect(midbottom = (randint(850,900), _y_pos))

        if score > 150:
            self.speed = 6
        elif score > 300:
            self.speed = 7
        elif score > 1000:
            self.speed = 8
                    
    def obstacle_animation(self):
        self.type_index += 0.1
        if self.type_index >= len(self.frames): self.type_index = 0
        self.image = self.frames[int(self.type_index)]

    def update(self):
        self.obstacle_animation()
        self.rect.x -= self.speed
        self.destroy_obstacle()
            
    def destroy_obstacle(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 100) - start_time
    score_surf = pixel_font.render(f'Score: {current_time} ', False, "gray0")
    score_rect = score_surf.get_rect(center = ((screen.get_width() / 2), 50))
    screen.blit(score_surf, score_rect)
    return current_time  

def sprite_collision():
    if pygame.sprite.spritecollide(player.sprite, obstacles_group, False):
        obstacles_group.empty()
        return False
    else: return True          
        
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("test_game")
clock = pygame.time.Clock()

start_time = 0
score = 0
best_score = 0
game_active = False

# Player sprite
player = pygame.sprite.GroupSingle()
player.add(Player(scale_factor=3))

# Enemies sprite
obstacles_group = pygame.sprite.Group()

# Text font settings
pixel_font = pygame.font.Font("font\pixel.ttf", 26)
title_font = pygame.font.Font("font\daydream.ttf", 50)

# Sky and ground graphics
sky_surface = pygame.image.load(fr"graphics\sky.png")
ground_surface = pygame.image.load("graphics\ground.png")

# Title screen
# Game title name
title_surf = title_font.render(f'Pixel Runner', False, "aquamarine2")
title_rect = title_surf.get_rect(center = ((screen.get_width() / 2), 200))

# Instructions to start the game
start_text_surf = pixel_font.render(f'Press [space] to start', False, "aquamarine2")
start_text_rect = start_text_surf.get_rect(center = ((screen.get_width() / 2), 300))

# Timer(event) for how often enemies to spawn
obstacle_timer = pygame.USEREVENT + 1 # custom user event
pygame.time.set_timer(obstacle_timer, 1350)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == obstacle_timer:
                if score > 150:
                    obstacles_group.add(Obstacle(choice(['fly','fly','snail','fly','snail','snail']), score))
                else:
                    obstacles_group.add(Obstacle(choice(['snail','snail','snail']), score))
        else:   
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 100)
                #print(start_time)
                

    if game_active:

        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()

        player.draw(screen)
        player.update()

        # This code is for debugging the player and the collision.
        #pygame.draw.rect(screen, (255, 0, 0), player.sprite.rect, 2)
        
        obstacles_group.draw(screen)
        obstacles_group.update()

        game_active = sprite_collision()

    else:
        # state where game is not active also title screen
        if score > best_score:  best_score = score

        screen.fill((94,129,162))
        screen.blit(title_surf,title_rect)
        
        clicking_time = pygame.time.get_ticks()
        if (clicking_time // 400) % 2 == 0: screen.blit(start_text_surf, start_text_rect)
        
        best_score_surf = pixel_font.render(f'Best score: {best_score} ', False, "aquamarine2")
        best_score_rect = best_score_surf.get_rect(center = ((screen.get_width() / 2), 380))
        screen.blit(best_score_surf, best_score_rect)

    pygame.display.update()
    clock.tick(60)
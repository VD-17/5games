# Movement 
# framerate is dependent speed of the computer
# Vectors to store direction 
# Vector is basically a list with 2 values: x and y. You can read and change the values 
# delta time make the movement framerate independent (depending on the compiter the game could run at very different framerate)
# Delta time: the time it took your computer to render the current fram

# sprites - best way to use classes in pygame
# It is an inbuild pygame class that always contains a surface and a rect 

import pygame
from os.path import join 
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = 

# general setup 
pygame.init()

# display_surface = pygame.display.set_mode((width, height)) 
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock() # can control the framerate and 

# plain surface 
surf = pygame.Surface((100, 200))
surf.fill("orange")
x = 100

# importing an image 
# path = join("images", "player.png") 
player_surface = pygame.image.load(join("images", "player.png")).convert_alpha()
player_rect = player_surface.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
player_direction = pygame.math.Vector2() 
player_speed = 300 

# meteor 
meteor_surface = pygame.image.load(join("images", "meteor.png")).convert_alpha()
meteor_rect = meteor_surface.get_frect(bottomright = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# laser 
laser_surface = pygame.image.load(join("images", "laser.png")).convert_alpha()
laser_rect = meteor_surface.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))

# Star image 
star_surface = pygame.image.load(join("images", "star.png")).convert_alpha()
star_positions = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(20)]

# rect 
# plain_rect = pygame.FRect(left, top, width, height)  

while running: 
    dt = clock.tick() / 1000 # delta time is in miliseconds and divide by 1000 to get in seconds 
    # print(clock.get_fps()) 

    # event loop 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if event.type == pygame.KEYDOWN:
        #     print()

        # if event.type == pygame.MOUSEMOTION:
        #     # print(event.pos)
        #     player_rect.center = event.pos
            
    # input 
    # pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    # if keys[pygame.K_RIGHT]: 
    #     player_direction.x = 1
    # else: 
    #     player_direction.x = 0
    player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

    recent_keys = pygame.key.get_just_pressed()
    if recent_keys[pygame.K_SPACE]:
        print("Fire laser")

    # normalize the direction when going diagnol so that the speed is the same  
    player_direction = player_direction.normalize() if player_direction else player_direction

    player_rect.center += player_direction * player_speed * dt  
    # print((player_direction * player_speed).magnitude())
    
    # draw the game
    # fill the window with color
    display_surface.fill('darkblue')

    for pos in star_positions:
        display_surface.blit(star_surface, pos)

    # player_rect.left += 0.1

    # player movement 
    # player_rect.x += player_direction * 100 
    # player_rect.x += 20 
    # player_rect.y -= 10 
    # if player_rect.bottom >= WINDOW_HEIGHT:
    #     player_rect.bottom = WINDOW_HEIGHT
    #     player_direction.y = -1
    # if player_rect.bottom >= WINDOW_HEIGHT or player_rect.top <= 0:
    #     player_direction.y *= -1 
    # if player_rect.right >= WINDOW_WIDTH or player_rect.left <= 0:
    #     player_direction.x *= -1 
    # player_rect.center += player_direction * player_speed * dt
    # if player_rect.right > WINDOW_WIDTH or player_rect.  left < 0:
    #     player_direction *= -1
    # x += 0.1 

    display_surface.blit(laser_surface, laser_rect)
    display_surface.blit(meteor_surface, meteor_rect)
    display_surface.blit(player_surface, player_rect)

    pygame.display.flip()
 
pygame.quit()
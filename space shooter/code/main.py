# Movement 
# framerate is dependent speed of the computer
# Vectors to store direction 
# Vector is basically a list with 2 values: x and y. You can read and change the values 
# delta time make the movement framerate independent (depending on the compiter the game could run at very different framerate)
# Delta time: the time it took your computer to render the current fram

# sprites - best way to use classes in pygame
# It is an inbuild pygame class that always contains a surface and a rect 
# pygame group to display sprites - draw, update and organize sprites 

# using a mask 
# An object that checks which pixels of a surface are visible 

# transforming surface - scale, flip, rotate, blur 

import pygame
from os.path import join 
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        # self.original_surf = pygame.image.load(join("images", "player.png")).convert_alpha()
        self.image = pygame.image.load(join("images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300

        # timer (cooldown)
        self.can_shoot = True 
        self.laser_shoot_time = 0
        self.cooldown_duration = 400 

        # transform test 
        # self.image = pygame.transform.rotate(self.image, 90)
        # self.image = pygame.transform.scale2x(self.image) 
        # self.image = pygame.transform.grayscale(self.image) 
        # self.rotation = 0

        # mask 
        self.mask = pygame.mask.from_surface(self.image)
        # mask_surf = mask.to_surface()
        # mask_surf.set_colorkey((0, 0, 0))
        # self.image = mask_surf

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks() 
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True 

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

        self.laser_timer()

        # continous rotation 
        # self.rotation += 20 * dt 
        # self.image = pygame.transform.rotate(self.original_surf, self.rotation)
            
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0: 
            self.kill() 

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf 
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        self.mask = pygame.mask.from_surface(self.image)
        self.rotation_speed = randint(40, 80)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)
        explosion_sound.play()

    def update(self, dt):
        self.frame_index += 5 * dt 
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)] 
        else:
            self.kill()

def collisions(): 
    global running
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        damage_sound.play()
        running = False
        
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites: 
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)

def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True, (255, 255, 255))
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (240, 240, 240), text_rect.inflate(20, 16).move(0, -8), 5, 10)

# general setup 
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()

# import 
star_surf = pygame.image.load(join("images", "star.png")).convert_alpha()
laser_surf = pygame.image.load(join("images", "laser.png")).convert_alpha()
meteor_surf = pygame.image.load(join("images", "meteor.png")).convert_alpha()
# font = pygame.font.Font(font, size)
# font = pygame.font.Font(None, 20)
# import font
font = pygame.font.Font(join("images", "Oxanium-Bold.ttf"), 40) 
explosion_frames = [pygame.image.load(join("images", "explosion", f"{i}.png")).convert_alpha() for i in range(21)]

laser_sound = pygame.mixer.Sound(join("audio", "laser.wav"))
laser_sound.set_volume(0.5)

explosion_sound = pygame.mixer.Sound(join("audio", "explosion.wav"))
damage_sound = pygame.mixer.Sound(join("audio", "damage.ogg"))
game_music = pygame.mixer.Sound(join("audio", "game_music.wav"))
game_music.set_volume(0.4)
game_music.play(loops = -1)

# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(20):
    Star(all_sprites, star_surf)

player = Player(all_sprites)

# custom events -> meteor event 
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

# test_rect = pygame.FRect(0, 0, 300, 600)

while running: 
    dt = clock.tick() / 1000

    # event loop 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))

    # to display and update the player 
    all_sprites.update(dt)

    collisions()

    display_surface.fill('#3a2e3f')

    display_score()

    all_sprites.draw(display_surface)

    # draw test 
    # pygame.draw.line(display_surface, 'red', (0, 0), (500, 600), 10)
    # pygame.draw.line(display_surface, 'red', (0, 0), pygame.mouse.get_pos(), 10)
    # pygame.draw.aaline(display_surface, 'red', (0, 0), (500, 600))

    # test collision 
    # player.rect.collidepoint(x, y)
    # player.rect.colliderect(test_rect) 

    pygame.display.flip()
 
pygame.quit()
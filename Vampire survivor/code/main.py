from settings import *
from player import Player
from sprites import *
from groups import AllSprites

from random import randint, choice 
from pytmx.util_pygame import load_pygame 


class Game: 
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Survivor")
        self.clock = pygame.time.Clock()
        self.running = True 

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = AllSprites()
        self.bullet_sprites = AllSprites()
        self.enemy_sprites = AllSprites()

        # gun timer 
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

        # enemy timer 
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 100)
        self.spawn_positions = []

        # audio 
        self.shoot_sound = pygame.mixer.Sound(join("audio", "shoot.wav"))
        self.shoot_sound.set_volume(0.4)
        self.impact_sound = pygame.mixer.Sound(join("audio", "impact.ogg"))
        self.music = pygame.mixer.Sound(join("audio", "music.wav"))
        self.music.set_volume(0.3)
        self.music.play(loops = -1)

        self.load_images()
        self.setup()

        # sprites
        # self.player = Player((500, 300), self.all_sprites, self.collision_sprites) # only has access to self.collision sprites 

        # for i in range(6):
        #     x, y = randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
        #     w, h = randint(60, 100), randint(50, 100)
        #     CollisionSprite((x, y), (w, h), (self.all_sprites, self.collision_sprites))

    def load_images(self):
        self.bullet_surf = pygame.image.load(join("images", "gun", "bullet.png")).convert_alpha()

        folders = list(walk(join("images", "enemies")))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join("images", "enemies", folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key = lambda name: int(name .split(".")[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)


    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot_sound.play()
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False 
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def setup(self):
        map = load_pygame(join("data", "maps", "world.tmx"))

        for x, y, image in map.get_layer_by_name("Ground").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name("Objects"): 
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name("Collisions"):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Player": 
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites) 
                self.gun = Gun(self.player, self.all_sprites)
            else: 
                self.spawn_positions.append((obj.x, obj.y))

    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                self.collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if self.collision_sprites:
                    self.impact_sound.play()
                    for sprite in self.collision_sprites:
                        sprite.destroy()
                    bullet.kill()

    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False

    def run(self):
        while self.running: 
            # dt
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
                if event.type == self.enemy_event:
                    Enemy(choice(self.spawn_positions), choice(list(self.enemy_frames.values())), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

            # update 
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)
            self.bullet_collision()
            self.player_collision()

            # draw 
            self.display_surface.fill("black")
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
            
        pygame.quit() 

if __name__ == "__main__":
    game = Game()
    game.run()

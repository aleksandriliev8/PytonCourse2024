import os
import sys
import math
import random

import pygame

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.button import Button

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Ninja game')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur = 6),
            'player/run': Animation(load_images('entities/player/run'), img_dur = 4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
        }

        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
        }

        self.sfx['ambience'].set_volume(0.2)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.7)

        self.clouds = Clouds(self.assets['clouds'], count = 16)

        self.player = Player(self, (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)

        self.load_level(0)

        self.level = 0
        self.screenshake = 0

        self.level_start_time = pygame.time.get_ticks()
        self.pause_start_time = 0
        self.total_paused_time = 0

        self.health = 3
        self.full_heart = pygame.image.load('assets/heart.png')

        self.star = pygame.image.load('assets/star.png')

    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))

        self.projectiles = []
        self.particles = []
        self.sparks = []

        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30

    def play(self):
        running = True

        while running:
            self.display.fill((0, 0, 0, 0))
            self.display_2.blit(self.assets['background'], (0, 0))

            self.screenshake = max(0, self.screenshake - 1)

            if not len(self.enemies):
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                    self.load_level(self.level)
                    self.total_paused_time = 0

            if self.transition < 0:
                self.transition += 1

            if self.dead:
                self.dead += 1
                if self.dead >= 10:
                    self.transition = min(30, self.transition + 1)
                if self.dead > 40:
                    self.health -= 1

                    if self.health == 0:
                        self.level = 0
                        self.health = 3
                        self.load_level(0)  
                    else:
                        self.load_level(self.level)
                    self.dead = 0

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame = random.randint(0, 20)))

            self.clouds.update()
            self.clouds.render(self.display_2, offset = render_scroll)

            self.tilemap.render(self.display, offset = render_scroll)

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)
            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset = render_scroll)

            # [[x, y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        self.sfx['hit'].play()
                        self.screenshake = max(16, self.screenshake)
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))

            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display_2.blit(display_sillhouette, offset)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True

                    if event.key == pygame.K_UP:
                        if self.player.jump():
                           self.sfx['jump'].play() 

                    if event.key == pygame.K_x:
                        self.player.dash()
                    
                    if event.key == pygame.K_q:
                        self.pause()
                        self.movement = [False, False]

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255,255,255))
                self.display.blit(transition_surf, (0, 0))

            self.display_2.blit(self.display, (0, 0))

            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), screenshake_offset)

            elapsed_time = (pygame.time.get_ticks() - self.level_start_time - self.total_paused_time) / 1000

            time_text = self.get_font(20).render(f"Time: {elapsed_time:.2f}s", True, "#ffe933")

            self.screen.blit(time_text, (20, 20))
            self.full_hearts()
            self.stars()

            pygame.display.update()
            self.clock.tick(60)

    def get_font(self, size):
        return pygame.font.Font("data/font.ttf", size)

    def main_menu(self):
        while True:
            mpos = pygame.mouse.get_pos()
            menu_text = self.get_font(60).render("NINJA GAME", True, (0,0,0))
            MENU_RECT = menu_text.get_rect(center=(320, 90))

            self.display.blit(self.assets['background'], (0, 0))
            
            self.clouds.update()
            self.clouds.render(self.display, (0, 0))
            
            play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(320, 200), 
                            text_input="PLAY", font= self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            options_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(320, 280), 
                                text_input="OPTIONS", font= self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(320, 360), 
                                text_input="QUIT", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            self.screen.blit(menu_text, MENU_RECT)

            for button in [play_button, options_button, quit_button]:
                button.changeColor(mpos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(mpos):
                        self.play()
                    if options_button.checkForInput(mpos):
                        pass
                    if quit_button.checkForInput(mpos):
                        pygame.quit()
                        sys.exit()

            self.clock.tick(60)

            pygame.display.update()

    def run(self):
        pygame.mixer.music.load('data/music.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.sfx['ambience'].play(-1)

        self.main_menu()

    def pause(self):
        self.pause_start_time = pygame.time.get_ticks()

        while True:            
            mpos = pygame.mouse.get_pos()

            self.display.blit(self.assets['background'], (0, 0))
            
            self.clouds.update()
            self.clouds.render(self.display, (0, 0))

            blur_surf = pygame.transform.smoothscale(self.display, (self.display.get_width() // 3, self.display.get_height() // 3))
            blur_surf = pygame.transform.smoothscale(blur_surf, self.display.get_size())

            self.screen.blit(pygame.transform.scale(blur_surf, self.screen.get_size()), (0, 0))
            
            play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(320, 150), 
                            text_input="LEVELS", font= self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            options_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(320, 250), 
                                text_input="OPTIONS", font= self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(320, 350), 
                                text_input="QUIT", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")

            for button in [play_button, options_button, quit_button]:
                button.changeColor(mpos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.total_paused_time += pygame.time.get_ticks() - self.pause_start_time
                        return 

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(mpos):
                        self.total_paused_time += pygame.time.get_ticks() - self.pause_start_time
                        self.play()
                    if options_button.checkForInput(mpos):
                        pass
                    if quit_button.checkForInput(mpos):
                        pygame.quit()
                        sys.exit()

            self.clock.tick(60)

            pygame.display.update()

    def stars(self):
        screen_width = self.screen.get_width() 
        star_spacing = 35

        elapsed_time = (pygame.time.get_ticks() - self.level_start_time - self.total_paused_time) / 1000

        if elapsed_time < 60:
            star_count = 3
        elif elapsed_time < 90:
            star_count = 2
        else:
            star_count = 1

        total_width = star_count * star_spacing
        start_x = (screen_width - total_width) / 2

        for i in range(star_count):
            x_pos = start_x + i * star_spacing
            self.screen.blit(self.star, (x_pos, 10))


    def full_hearts(self):
        screen_width = self.screen.get_width() 
        heart_spacing = 38

        for i in range(self.health):
            x_pos = screen_width - (i + 1.5) * heart_spacing
            self.screen.blit(self.full_heart, (x_pos, 8))


Game().run()

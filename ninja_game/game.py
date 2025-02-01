import sys

import pygame

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Ninja game')
        # create window
        self.screen = pygame.display.set_mode((600, 480))

        self.clock = pygame.time.Clock()

        self.img = pygame.image.load('data/images/clouds/cloud_1.png')

    def run(self):
        while True:
            self.screen.blit(self.img, (100, 200))

            for event in pygame.event.get():
                #clicked x on the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            # run the loop at 60fps
            self.clock.tick(60)

Game().run()
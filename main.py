import pygame
import sys
from classes import *
from process import process

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 360
FPS = 64
total_frames = 0

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()

background = pygame.image.load("./images/background.png")
bug_01 = Bug(0, SCREEN_HEIGHT - 40, "./images/tank_right.png")
# enemy_01 = Enemy(0, 100, 40, 40, "./images/enemy_right.png")  # Now multiple Enemy generated in process.py
# enemy_02 = Enemy(0, 180, 40, 40, "./images/enemy_right.png")  # for simplicity

while not Bug.game_lost:
    process(bug_01, FPS, total_frames)

    # LOGIC
    bug_01.motion(SCREEN_WIDTH, SCREEN_HEIGHT)
    Enemy.update_all(SCREEN_WIDTH, SCREEN_HEIGHT)
    Fire.movement()
    total_frames += 1

    # DRAW
    screen.blit(background, (0, 0))  # Instead of bg color # screen.fill((0, 0, 0))
    BaseClass.all_sprites.draw(screen)
    Fire.List.draw(screen)
    pygame.display.flip()

    # LOOP TIMER
    clock.tick(FPS)

print "\n\n NO OF ENEMIES DESTROYED : %d\n\n" % BaseClass.enemy_destroyed
background = pygame.image.load("./images/lost_1.png")
while Bug.game_lost:
    screen.blit(background, (0, 0))  # Instead of bg color # screen.fill((0, 0, 0))
    BaseClass.all_sprites.draw(screen)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

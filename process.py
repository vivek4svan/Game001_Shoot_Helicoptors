import pygame
import sys
import classes
import random


# PROCESSING
def process(bug_01, fps, total_frames):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                classes.Fire.fire_type = not classes.Fire.fire_type

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
        classes.Bug.going_right = True
        bug_01.image = pygame.image.load("./images/tank_right.png")
        bug_01.vel_x = 5
    elif keys[pygame.K_a]:
        classes.Bug.going_right = False
        bug_01.image = pygame.image.load("./images/tank_left.png")
        bug_01.vel_x = -5
    else:
        bug_01.vel_x = 0

    if keys[pygame.K_w]:
        bug_01.image = pygame.image.load("./images/tank_up.png")
        bug_01.vel_y = -5

    elif keys[pygame.K_s]:
        bug_01.image = pygame.image.load("./images/tank_down.png")
        bug_01.vel_y = 5

    else:
        bug_01.vel_y = 0

    # Enable below if statement if you want to enable jumping feature
    # if keys[pygame.K_j]:
    #     bug_01.jumping = True

    if keys[pygame.K_SPACE]:
        def direction():
            if classes.Bug.going_right:
                p.vel_x = 8
            else:
                p.image = pygame.transform.flip(p.image, True, False)
                p.vel_x = -8
            classes.Fire.shoot = False

        if classes.Fire.fire_type and classes.Fire.shoot:
            p = classes.Fire(bug_01.rect.x, bug_01.rect.y + 18, "./images/bullet_1.png", "destroy")
            direction()
        elif not classes.Fire.fire_type and classes.Fire.shoot:
            p = classes.Fire(bug_01.rect.x, bug_01.rect.y + 18, "./images/bullet_2.png", "freeze")
            direction()

    spawn(fps, total_frames)
    collisions()
    check_shoot_timer()


def check_shoot_timer():
    if not classes.Fire.shoot and classes.Fire.blank_shoot_counter != 12:
        classes.Fire.blank_shoot_counter += 1
    else:
        classes.Fire.shoot = True
        classes.Fire.blank_shoot_counter = 0


def spawn(fps, total_frames):
    four_seconds = fps * 2

    if total_frames % four_seconds == 0:
        r = random.randint(1, 2)
        x = 1
        if r == 2:
            x = 640 - 40
        classes.Enemy(x, 100, "./images/enemy_right.png")


# We will be using sprite functionality for collision detection
def collisions():
    # pygame.sprite.groupcollide(group_1, group_2, dokill_1, dokill_2)  # Method, we are not using this for now
    for enemy in classes.Enemy.List:
        # We are using this (Object, Group, Kill)
        collide = pygame.sprite.spritecollide(enemy, classes.Fire.List, True)
        if collide:
            if collide[0].shoot_type == "destroy":
                enemy.health -= enemy.half_health
            else:
                enemy.vel_x = 0

    # For destroying the missile if set False in above [As in tutorial to maintain close shoot]
    # But i Have maintained it shooting times as other logic so True above, No need for below.
    for missile in classes.Fire.List:
        if pygame.sprite.spritecollide(missile, classes.Fire.List, False):
            pass
    # # For detecting Self Death
    for enemy in classes.Enemy.List:
        if pygame.sprite.spritecollide(enemy, classes.Bug.List, True):
            classes.Bug.game_lost = True

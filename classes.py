import pygame
import math
from random import randint


# pygame.sprite.Sprite : Contains everything for collision det, Movements etc
class BaseClass(pygame.sprite.Sprite):
    all_sprites = pygame.sprite.Group()
    enemy_destroyed = 0

    def __init__(self, x, y, image_string):
        pygame.sprite.Sprite.__init__(self)
        BaseClass.all_sprites.add(self)
        self.image = pygame.image.load(image_string)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def destroy(self, class_name):
        class_name.List.remove(self)
        BaseClass.all_sprites.remove(self)
        del self
        BaseClass.enemy_destroyed += 1


class Bug(BaseClass):
    List = pygame.sprite.Group()
    going_right = True
    game_lost = False

    def __init__(self, x, y, image_string):
        BaseClass.__init__(self, x, y, image_string)
        Bug.List.add(self)
        self.vel_x, self.vel_y = 0, 0
        self.jump_y = 5
        self.jumping, self.go_down = False, False
        self.shoot = False

    def motion(self, screen_width, screen_height):
        predicted_loc_x = self.rect.x + self.vel_x
        predicted_loc_y = self.rect.y + self.vel_y

        if predicted_loc_x < 0:
            self.vel_x = 0
        elif predicted_loc_x + self.rect.width > screen_width:
            self.vel_x = 0
        if predicted_loc_y < 0:
            self.vel_y = 0
        elif predicted_loc_y + self.rect.height > screen_height:
            self.vel_y = 0

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.__jump(screen_height)

    def __jump(self, screen_height):
        max_jump = 200

        if self.jumping:
            if self.rect.y < max_jump:
                self.go_down = True
            if self.go_down:
                self.rect.y += self.jump_y
                predicted_jump_y = self.rect.y + self.jump_y
                if predicted_jump_y + self.rect.height > screen_height:
                    self.jumping = False
                    self.go_down = False
            else:
                self.rect.y -= self.jump_y


class Enemy(BaseClass):
    List = pygame.sprite.Group()

    def __init__(self, x, y, image_string):
        BaseClass.__init__(self, x, y, image_string)
        Enemy.List.add(self)
        self.health = 100
        self.half_health = self.health / 1.0
        self.vel_x = randint(1, 4)
        self.amplitude, self.period = randint(20, 80), randint(4, 5) / 100.0

    def fly(self, screen_width, screen_height):
        if self.rect.x + self.rect.width > screen_width or self.rect.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)  # Rotate on x=True y=False
            self.vel_x = -self.vel_x  # Reverse the direction also once right/left limit reached
            # amplitude * sin(period * x_pos + shift) + y_high = sine curve
        self.rect.y = self.amplitude * math.sin(self.period * self.rect.x) + 140
        self.rect.x += self.vel_x

    @staticmethod
    def update_all(screen_width, screen_height):
        for enemy in Enemy.List:
            enemy.fly(screen_width, screen_height)
            if enemy.health <= 0:
                enemy.destroy(Enemy)

#    @staticmethod
#    def movement(screen_width, screen_height):  # Moved to update_all() function
#        for enemy in Enemy.List:
#            enemy.fly(screen_width, screen_height)


class Fire(pygame.sprite.Sprite):
    List = pygame.sprite.Group()
    shoot = True
    blank_shoot_counter = 0
    fire_type = True

    def __init__(self, x, y, image_string, shoot_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_string)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shoot_type = shoot_type
        self.vel_x = None
        Fire.List.add(self)

        # try:
        #     last_element = Fire.normal_list[-1]
        #     difference = abs(self.rect.x - last_element.rect.x)
        #     if difference < self.rect.width:
        #         return
        # except Exception:
        #     pass

    @staticmethod
    def movement():
        for projectile in Fire.List:
            projectile.rect.x += projectile.vel_x

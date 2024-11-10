import pygame
import path
import animation
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, animations, x, y, frame_rate, action):
        super().__init__()
        self.animations = animations  # *****字典：动作名称 -> 动作帧列表*****
        self.current_action = action
        self.frames = self.animations[self.current_action]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.frame_rate = frame_rate
        self.last_updated = pygame.time.get_ticks()
        self.mask = pygame.mask.from_surface(self.image)
    def set_action(self, action_name):
        if action_name in self.animations and action_name != self.current_action:
            self.current_action = action_name
            self.frames = self.animations[self.current_action]
            self.current_frame = 0
            self.image = self.frames[self.current_frame]
            self.mask = pygame.mask.from_surface(self.image)
            self.last_updated = pygame.time.get_ticks()
    def update(self):
        now = pygame.time.get_ticks()
        if self.current_action == 'dead' or self.current_action == 'wood' or self.current_action == 'tree_trunk':
            if now - self.last_updated > self.frame_rate:
                if self.current_frame < len(self.frames) - 1:
                    self.current_frame += 1
                    self.image = self.frames[self.current_frame]
                    self.mask = pygame.mask.from_surface(self.image)
                    self.last_updated = now
        else:
            if now - self.last_updated > self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
                self.mask = pygame.mask.from_surface(self.image)
                self.last_updated = now
class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed):
        super().__init__()
        self.image_path = path.arrow
        self.image = animation.load_image(self.image_path)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.speed = speed
        self.direction = direction
        self.mask = pygame.mask.from_surface(self.image)
        self.collide_flag=0
        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)
    def update(self):
        if self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
class Player(AnimatedSprite):
    def __init__(self, animations, x, y, frame_rate, action):
        super().__init__(animations, x, y, frame_rate, action)
        self.live =True
        self.speed = 5
        self.orient = 'right'
        self.wood = 2
        self.score = 0
        self.last_hurt_time = 0
        self.current_health = 1000
        self.max_health = 1000
        self.health_length = 80

    def update_healthbar(self):
        # 血条
        self.health_surf = pygame.Surface((self.health_length, 5))
        self.health_rect = self.health_surf.get_rect(midtop=self.rect.midtop)

        self.currenthealth_surf = pygame.Surface((self.current_health/self.max_health*80,5))
        self.currenthealth_rect = self.health_surf.get_rect(topleft=self.health_rect.topleft)

        self.health_surf.fill('black')
        self.currenthealth_surf.fill('red')

    def get_orient(self):
        orient_right = ['walk_right', 'shoot_right', 'still_right','attack_right']
        orient_left = ['walk_left', 'shoot_left', 'still_left','attack_left']
        orient_up = ['walk_up','attack_up']
        orient_down = ['walk_down','attack_down']
        if self.current_action in orient_right:
            self.orient = 'right'
        if self.current_action in orient_left:
            self.orient = 'left'
        if self.current_action in orient_up:
            self.orient = 'up'
        if self.current_action in orient_down:
            self.orient = 'down'
class Warrior(Player):
    def __init__(self, animations, x, y, frame_rate, action):
        super().__init__(animations, x, y, frame_rate, action)
        self.orient = 'right'
        self.last_sword_time = 0
class Archer(Player):
    def __init__(self, animations, x, y, frame_rate, action):
        super().__init__(animations, x, y, frame_rate, action)
        self.orient = 'left'
        self.last_shot_time = 0
    def shoot_arrow(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= 795:
            arrow = Arrow(self.rect.centerx + 40, self.rect.centery + 5, self.orient, 5)
            self.last_shot_time = now
            return arrow    #即使它们的名称相同，它们仍然是不同的对象。也就是说，精灵名称不会影响它们的唯一性，因为每个精灵都有一个独立的内存地址和对象引用。
        return None
class Tree(AnimatedSprite):
    def __init__(self, animations, x, y, frame_rate, action):
        super().__init__( animations, x, y, frame_rate, action)
        self.live=True
        self.current_health = 1000
        self.last_hurt_time=0
        self.id = id

class Wood(AnimatedSprite):
    def __init__(self, animations, x, y, frame_rate, action):
        super().__init__(animations, x, y, frame_rate, action)
        self.fall_time=pygame.time.get_ticks()
class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf):
        super().__init__()
        self.image = surf
        self.rect =self.image.get_rect(topleft = pos )
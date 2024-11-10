import pygame
from sys import exit
from animation import warrior_animations, archer_animations, tree_animations, wood_animations
import path
from my_class import Warrior, Archer, Tree, Tile, Wood
import random
import math
from pytmx.util_pygame import load_pygame

from utils import resource_path

pygame.init()
w, h = 192 * 7, 192 * 5
# 引入字体类型
f = pygame.font.Font(resource_path('simhei.ttf'), 40)
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('ArcherWarrior')
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load(path.bgm_file)
pygame.mixer.music.play(-1)

hurt = pygame.mixer.Sound(path.hurt_sound)
jump = pygame.mixer.Sound(path.jump_sound)
tap = pygame.mixer.Sound(path.tap_sound)
sword = pygame.mixer.Sound(path.sword_sound)
arch = pygame.mixer.Sound(path.arch_sound)
hit = pygame.mixer.Sound(path.Hit_sound)

def set_boundary(sprite):
    if sprite.rect.centerx < 448:
        if sprite.rect.centery < 448:
            sprite.rect.centerx = max(38, sprite.rect.centerx)
            sprite.rect.centery = max(38, sprite.rect.centery)
        else:
            sprite.rect.centerx = max(38, min(sprite.rect.centerx, 448 - 38))
            sprite.rect.centery = min(sprite.rect.centery, h - 38)
    elif sprite.rect.centerx > 896:
        if sprite.rect.centery < 448:
            sprite.rect.centerx = min(sprite.rect.centerx, w - 38)
            sprite.rect.centery = max(38, sprite.rect.centery)
        else:
            sprite.rect.centerx = max(896 + 38, min(sprite.rect.centerx, w - 38))
            sprite.rect.centery = min(sprite.rect.centery, h - 38)
    else:
        sprite.rect.centery = max(38, min(sprite.rect.centery, 448 - 38))


def set_text(Archer_score, Warrior_score, Archer_wood, Warrior_wood):
    # 生成文本信息，第一个参数文本内容；第二个参数，字体是否平滑；
    # 第三个参数，RGB模式的字体颜色；第四个参数，RGB模式字体背景颜色；
    Archer_score_text = f.render("Archer_score:" + str(Archer_score), True, (255, 255, 255), )
    # 获得显示对象的rect区域坐标
    Archer_score_textRect = Archer_score_text.get_rect()
    # 设置显示对象居中
    Archer_score_textRect.x, Archer_score_textRect.y = (192 * 5, 0)

    Warrior_score_text = f.render("Warrior_score:" + str(Warrior_score), True, (255, 255, 255))
    # 获得显示对象的rect区域坐标
    Warrior_score_textRect = Warrior_score_text.get_rect()
    # 设置显示对象居中
    Warrior_score_textRect.x, Warrior_score_textRect.y = (64, 0)
    # -----------------------------------------------------------
    Archer_wood_text = f.render("Archer_wood:" + str(Archer_wood), True, (255, 255, 255), )
    # 获得显示对象的rect区域坐标
    Archer_wood_textRect = Archer_wood_text.get_rect()
    # 设置显示对象居中
    Archer_wood_textRect.x, Archer_wood_textRect.y = (192 * 5, 0 + 64)

    Warrior_wood_text = f.render("Warrior_wood:" + str(Warrior_wood), True, (255, 255, 255))
    # 获得显示对象的rect区域坐标
    Warrior_wood_textRect = Warrior_wood_text.get_rect()
    # 设置显示对象居中
    Warrior_wood_textRect.x, Warrior_wood_textRect.y = (64, 0 + 64)
    board = {
        'score': {
            'text': [Warrior_score_text, Archer_score_text],
            'rect': [Warrior_score_textRect, Archer_score_textRect]
        },
        'wood': {
            'text': [Warrior_wood_text, Archer_wood_text],
            'rect': [Warrior_wood_textRect, Archer_wood_textRect]
        }
    }
    return board
    # -----------------------------------------------------------


def key_archer(keys, archer, arrow_group):
    if archer.live:
        if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            archer.rect.y += archer.speed / math.sqrt(2)
            archer.rect.x += archer.speed / math.sqrt(2)
            archer.set_action('walk_right')

        elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            archer.rect.y -= archer.speed / math.sqrt(2)
            archer.rect.x += archer.speed / math.sqrt(2)
            archer.set_action('walk_right')
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            archer.rect.y += archer.speed / math.sqrt(2)
            archer.rect.x -= archer.speed / math.sqrt(2)
            archer.set_action('walk_left')
        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            archer.rect.y -= archer.speed / math.sqrt(2)
            archer.rect.x -= archer.speed / math.sqrt(2)
            archer.set_action('walk_right')

        elif keys[pygame.K_DOWN]:
            archer.rect.y += archer.speed
            archer.set_action('walk_right')
        elif keys[pygame.K_UP]:
            archer.rect.y -= archer.speed
            archer.set_action('walk_right')
        elif keys[pygame.K_LEFT]:
            archer.rect.x -= archer.speed
            archer.set_action('walk_left')
        elif keys[pygame.K_RIGHT]:
            archer.rect.x += archer.speed
            archer.set_action('walk_right')
        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            archer.rect.y += archer.speed
            archer.rect.x += archer.speed
            archer.set_action('walk_right')
        elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            archer.rect.y -= archer.speed
            archer.rect.x += archer.speed
            archer.set_action('walk_right')
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            archer.rect.y += archer.speed
            archer.rect.x -= archer.speed
            archer.set_action('walk_left')
        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            archer.rect.y -= archer.speed
            archer.rect.x -= archer.speed
            archer.set_action('walk_right')

        elif keys[pygame.K_l]:
            archer.get_orient()
            if archer.orient == 'left':
                archer.set_action('shoot_left')
                arch_now_time = pygame.time.get_ticks()
                if arch_now_time - archer.last_shot_time > 795:
                    arch.play()
            if archer.orient == 'right':
                archer.set_action('shoot_right')
                arch_now_time = pygame.time.get_ticks()
                if arch_now_time - archer.last_shot_time > 795:
                    arch.play()
            arrow = archer.shoot_arrow()  # 即使它们的名称相同，它们仍然是不同的对象。也就是说，精灵名称不会影响它们的唯一性，因为每个精灵都有一个独立的内存地址和对象引用。
            if arrow:
                arrow_group.add(arrow)

        else:
            archer.get_orient()
            if archer.orient == 'left':
                archer.set_action('still_left')
            if archer.orient == 'right':
                archer.set_action('still_right')
            else:
                archer.set_action('still_left')


# --------------------
def key_warrior(keys, warrior):
    if warrior.live:
        if keys[pygame.K_s] and keys[pygame.K_d]:
            warrior.rect.y += warrior.speed / math.sqrt(2)
            warrior.rect.x += warrior.speed / math.sqrt(2)
            warrior.set_action('walk_right')
        elif keys[pygame.K_w] and keys[pygame.K_d]:
            warrior.rect.y -= warrior.speed / math.sqrt(2)
            warrior.rect.x += warrior.speed / math.sqrt(2)
            warrior.set_action('walk_right')
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            warrior.rect.y += warrior.speed / math.sqrt(2)
            warrior.rect.x -= warrior.speed / math.sqrt(2)
            warrior.set_action('walk_left')
        elif keys[pygame.K_w] and keys[pygame.K_a]:
            warrior.rect.y -= warrior.speed / math.sqrt(2)
            warrior.rect.x -= warrior.speed / math.sqrt(2)
            warrior.set_action('walk_left')
        elif keys[pygame.K_s]:
            warrior.rect.y += 5
            warrior.set_action('walk_right')
        elif keys[pygame.K_w]:
            warrior.rect.y -= 5
            warrior.set_action('walk_right')
        elif keys[pygame.K_a]:
            warrior.rect.x -= 5
            warrior.set_action('walk_left')
        elif keys[pygame.K_d]:
            warrior.rect.x += 5
            warrior.set_action('walk_right')

        elif keys[pygame.K_g]:
            warrior.get_orient()
            if warrior.orient == 'up' and keys[pygame.K_g]:
                warrior.set_action('attack_up')
                sword_now_time = pygame.time.get_ticks()
                if sword_now_time - warrior.last_sword_time > 600:
                    sword.play()
                    warrior.last_sword_time = pygame.time.get_ticks()
            if warrior.orient == 'down' and keys[pygame.K_g]:
                warrior.set_action('attack_down')
                if warrior.current_frame in [3, 4, 5, 6, 9, 10, 11]:
                    sword_now_time = pygame.time.get_ticks()
                    if sword_now_time - warrior.last_sword_time > 600:
                        sword.play()
                        warrior.last_sword_time = pygame.time.get_ticks()
            if warrior.orient == 'left':
                warrior.set_action('attack_left')
                sword_now_time = pygame.time.get_ticks()
                if sword_now_time - warrior.last_sword_time > 600:
                    sword.play()
                    warrior.last_sword_time = pygame.time.get_ticks()
            if warrior.orient == 'right':
                warrior.set_action('attack_right')
                if warrior.current_frame in [3, 4, 5, 6, 9, 10, 11]:
                    sword_now_time = pygame.time.get_ticks()
                    if sword_now_time - warrior.last_sword_time > 600:
                        sword.play()
                        warrior.last_sword_time = pygame.time.get_ticks()

        else:
            warrior.get_orient()
            if warrior.orient == 'left':
                warrior.set_action('still_left')
            else:
                warrior.set_action('still_right')

# --------------------
def main():
    # 对象创建-------------------
    player_group = pygame.sprite.Group()
    arrow_group = pygame.sprite.Group()
    tree_group = pygame.sprite.Group()
    wood_group = pygame.sprite.Group()
    map_group = pygame.sprite.Group()

    archer = Archer(archer_animations, w - 192, h / 2 - 192 / 2, 100, 'still_left')
    warrior = Warrior(warrior_animations, 0, h / 2 - 192 / 2, 100, 'still_right')
    player_group.add(archer)
    player_group.add(warrior)


    # 随机生成树
    tree_pos_list = [(random.randint(0, w - 192), random.randint(0, h - 192)) for _ in range(20)]
    tree_pos_list = [(x, y) for x, y in tree_pos_list if
                     not (448 - 192 / 2 - 20 <= x < 896 - 192 / 2 - 20 and 448 - 192 <= y < 960)]
    for tree_pos in tree_pos_list:
        tree = Tree(tree_animations, tree_pos[0], tree_pos[1], 200, 'tree_still')
        tree_group.add(tree)

    # map----
    tmx_data = load_pygame(resource_path(r'map\tmx\map.tmx'))
    for layer in tmx_data.visible_layers:
        if hasattr(layer, 'data'):
            for x, y, surf in layer.tiles():
                pos = x * 64, y * 64
                map = Tile(pos, surf)
                map_group.add(map)
    # -------
    # --------------------------
    while True:
        board = set_text(archer.score, warrior.score, archer.wood, warrior.wood, )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        key_archer(keys, archer, arrow_group)
        key_warrior(keys, warrior)
        # 碰撞----------------------------
        # arrow warrior 碰撞---
        for arrow in arrow_group.sprites():
            if warrior.live:
                if pygame.sprite.collide_mask(arrow, warrior):  # 碰撞，置1，得到碰撞时间arrow_collide_time
                    arrow_group.remove(arrow)
                    if (warrior.current_action == "attack_right" or warrior.current_action == "attack_left") and warrior.current_frame in [
                        3, 4, 5, 6, 9, 10, 11]:
                        tap.play()
                    elif keys[pygame.K_f]:
                        if warrior.wood:
                            wood = Wood(wood_animations, warrior.rect.x, warrior.rect.y, 100, 'wood')
                            wood.set_action('wood')
                            jump.play()
                            wood_group.add(wood)
                            warrior.wood -= 1
                            flag = random.randint(0, 1)
                            if flag == 1:
                                warrior.rect.y += 120
                            else:
                                warrior.rect.y -= 120
                        else:
                            warrior.current_health -= 200
                            hit.play()
                            if warrior.current_health <= 0:
                                warrior.set_action('dead')
                                warrior.hurt_time = pygame.time.get_ticks()
                                if warrior.hurt_time - warrior.last_hurt_time > warrior.frame_rate + 100:
                                    archer.score += 1
                                    hurt.play()
                                    warrior.last_hurt_time = warrior.hurt_time
                                warrior.live = False
                    else:
                        warrior.current_health -= 200
                        hit.play()
                        if warrior.current_health <= 0:
                            warrior.set_action('dead')
                            warrior.hurt_time = pygame.time.get_ticks()
                            if warrior.hurt_time - warrior.last_hurt_time > warrior.frame_rate + 100:
                                archer.score += 1
                                hurt.play()
                                warrior.last_hurt_time = warrior.hurt_time
                            warrior.live = False
        #  warrior archer 碰撞
        if pygame.sprite.collide_mask(warrior, archer):
            if warrior.current_action in ["attack_right", "attack_left"] and warrior.current_frame in [3, 4, 5, 6,
                                                                                                       9, 10,
                                                                                                       11] and archer.live:
                if keys[pygame.K_k] and archer.wood:
                    wood = Wood(wood_animations, archer.rect.x, archer.rect.y, 100, 'wood')
                    wood.set_action('wood')
                    jump.play()
                    wood_group.add(wood)
                    archer.wood -= 1
                    flag = random.randint(0, 1)
                    if flag == 1:
                        archer.rect.y += 120
                    else:
                        archer.rect.y -= 120
                else:
                    archer.hurt_time = pygame.time.get_ticks()
                    if archer.hurt_time - archer.last_hurt_time > archer.frame_rate + 300:
                        archer.current_health -= 100
                        hit.play()
                        archer.last_hurt_time = archer.hurt_time
                        if archer.current_health <= 0:
                            archer.set_action('dead')
                            warrior.score += 1
                            hurt.play()
                            archer.live = False

        # Warrior Tree 碰撞
        for tree in tree_group:
            if tree.live:
                if pygame.sprite.collide_mask(warrior, tree):
                    if warrior.current_action in ["attack_right", "attack_left"] and warrior.current_frame in [3, 4, 5,
                                                                                                               6, 9, 10,
                                                                                                               11]:
                        tree.hurt_time = pygame.time.get_ticks()
                        if tree.hurt_time-tree.last_hurt_time >tree.frame_rate +300:
                            tree.current_health -= 200
                            hit.play()
                            tree.last_hurt_time=tree.hurt_time
                            print(tree.current_health)
                        if tree.current_health<=0:
                            tree.set_action('tree_cut')
                            tree.live = False
            if tree.live == False and tree.current_frame == 6:
                tree.set_action('tree_trunk')
                wood = Wood(wood_animations, tree.rect.x, tree.rect.y, 100, 'wood')
                wood.set_action('wood')
                wood_group.add(wood)

        # Warrior Wood 碰撞
        for wood in wood_group:
            if pygame.sprite.collide_mask(warrior, wood):
                wood.pick_time = pygame.time.get_ticks()
                if wood.pick_time - wood.fall_time > 1000:
                    wood_group.remove(wood)
                    warrior.wood += 1
                    jump.play()
        # Archer Wood 碰撞
        for wood in wood_group:
            if pygame.sprite.collide_mask(archer, wood):
                wood.pick_time = pygame.time.get_ticks()
                if wood.pick_time - wood.fall_time > 1000:
                    wood_group.remove(wood)
                    archer.wood += 1
                    jump.play()
        # --------------------------------
        # 死亡移除---
        if archer.live == False and archer.current_frame == 13:  # ?
            player_group.remove(archer)
            archer = Archer(archer_animations, 192 * 7 - 192 / 2, 192 * 2.5 - 192 / 2, 100, 'still_left')
            player_group.add(archer)
        if warrior.live == False and warrior.current_frame == 13:
            player_group.remove(warrior)
            warrior = Warrior(warrior_animations, 0, 192 * 2.5 - 192 / 2, 100, 'still_right')
            player_group.add(warrior)
        if arrow_group:
            if arrow.rect.x > w or arrow.rect.x + 40 < 0:
                arrow_group.remove(arrow)
        # ----------
        # 边界检查
        set_boundary(archer)
        set_boundary(warrior)

        player_group.update()
        arrow_group.update()
        wood_group.update()
        tree_group.update()
        map_group.update()

        map_group.draw(screen)
        wood_group.draw(screen)
        tree_group.draw(screen)
        arrow_group.draw(screen)
        player_group.draw(screen)

        screen.blit(board['score']['text'][1], board['score']['rect'][1])
        screen.blit(board['score']['text'][0], board['score']['rect'][0])
        screen.blit(board['wood']['text'][1], board['wood']['rect'][1])
        screen.blit(board['wood']['text'][0], board['wood']['rect'][0])


        warrior.update_healthbar()
        screen.blit(warrior.health_surf, warrior.health_rect)
        screen.blit(warrior.currenthealth_surf,warrior.currenthealth_rect)

        archer.update_healthbar()
        screen.blit(archer.health_surf, archer.health_rect)
        screen.blit(archer.currenthealth_surf, archer.currenthealth_rect)
        pygame.mouse.set_visible(False)
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.image.load(resource_path("image/Mouse/01.png")).convert_alpha()
        screen.blit(mouse, mouse_pos)
        pygame.display.update()
        clock.tick(120)  # 一次循环最快 (1s/60fps)*1000 (ms)

if __name__ == "__main__":
    main()

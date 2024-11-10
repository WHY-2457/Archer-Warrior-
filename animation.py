import pygame
import path
import os

w, h = 192 * 7, 192 * 5  # ?
pygame.init()
screen = pygame.display.set_mode((w, h))


def load_image(path, scale_size=None):
    # 获取image
    try:
        image = pygame.image.load(path).convert_alpha()
        if scale_size:
            image = pygame.transform.scale(image, scale_size)
        return image
    except pygame.error as e:
        print(f"无法加载图像: {path}")
        raise SystemExit(e)


def load_animation_frames(path, frame_count, scale_size=None):
    # 获取动画帧列表
    frames = []
    for i in range(1, frame_count + 1):
        frame_path = path.format(i)
        frames.append(load_image(frame_path, scale_size))
    return frames


warrior_still_right_frames = load_animation_frames(path.warrior_still_right, 6, (192, 192))
warrior_still_left_frames = load_animation_frames(path.warrior_still_left, 6, (192, 192))
warrior_walk_right_frames = load_animation_frames(path.warrior_walk_right, 6, (192, 192))
warrior_walk_left_frames = load_animation_frames(path.warrior_walk_left, 6, (192, 192))
warrior_attack_right_frames = load_animation_frames(path.warrior_attack_right, 12, (192, 192))
warrior_attack_left_frames = load_animation_frames(path.warrior_attack_left, 12, (192, 192))
warrior_attack_up_frames = load_animation_frames(path.warrior_attack_up, 12, (192, 192))
warrior_attack_down_frames = load_animation_frames(path.warrior_attack_down, 12, (192, 192))
warrior_dead_frames = load_animation_frames(path.warrior_dead, 14, (192, 192))

warrior_animations = {
    'still_right': warrior_still_right_frames,
    'still_left': warrior_still_left_frames,
    'walk_right': warrior_walk_right_frames,
    'walk_left': warrior_walk_left_frames,
    'attack_right': warrior_attack_right_frames,
    'attack_left': warrior_attack_left_frames,
    'attack_up': warrior_attack_up_frames,
    'attack_down': warrior_attack_down_frames,
    'dead': warrior_dead_frames
}
archer_still_right_frames = load_animation_frames(path.archer_still_right, 6, (192, 192))
archer_still_left_frames = load_animation_frames(path.archer_still_left, 6, (192, 192))
archer_walk_right_frames = load_animation_frames(path.archer_walk_right, 6, (192, 192))
arhcer_walk_left_frames = load_animation_frames(path.archer_walk_left, 6, (192, 192))
archer_shoot_right_frames = load_animation_frames(path.archer_shoot_right, 8, (192, 192))
archer_shoot_left_frames = load_animation_frames(path.archer_shoot_left, 8, (192, 192))
archer_dead_frames = load_animation_frames(path.archer_archer_dead, 14, (192, 192))
# surface列表->动画
archer_animations = {
    'still_right': archer_still_right_frames,
    'still_left': archer_still_left_frames,
    'walk_right': archer_walk_right_frames,
    'walk_left': arhcer_walk_left_frames,
    'shoot_right': archer_shoot_right_frames,
    'shoot_left': archer_shoot_left_frames,
    'dead': archer_dead_frames
}
tree_still_frames = load_animation_frames(path.tree_still, 3, (192, 192))
tree_trunk_frames = load_animation_frames(path.tree_trunk, 1, (192, 192))
tree_cut_frames = load_animation_frames(path.tree_cut, 7, (192, 192))
# surface列表->动画
tree_animations = {
    'tree_still': tree_still_frames,
    'tree_trunk': tree_trunk_frames,
    'tree_cut': tree_cut_frames
}
wood_frames = load_animation_frames(path.Wood, 6, (192, 192))
wood_animations = {
    'wood': wood_frames
}

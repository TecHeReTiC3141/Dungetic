import pygame

def get_rect_dist(rect1: pygame.Rect, rect2: pygame.Rect):
    return rect1.centerx - rect2.centerx, rect1.centery - rect2.centery

def get_rect_abs_dist(rect1: pygame.Rect, rect2: pygame.Rect):
    pass
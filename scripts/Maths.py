import pygame


def get_rect_dist(rect1: pygame.Rect, rect2: pygame.Rect):
    return rect1.centerx - rect2.centerx, rect1.centery - rect2.centery


def get_rects_dir(rect1: pygame.Rect, rect2: pygame.Rect):
    """
    :param rect1: start rect
    :param rect2: target rect
    :return: normalized direction from start rect to target one
    """
    cent1, cent2 = pygame.math.Vector2(rect1.center), pygame.math.Vector2(rect2.center)
    print(cent2 - cent1, (cent2 - cent1).normalize())
    if (cent2 - cent1).length():
        return (cent2 - cent1).normalize()
    return cent2 - cent1

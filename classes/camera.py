from classes.Heretic import *

class Camera:

    def __init__(self, surface: pygame.Surface, player: Heretic):
        self.surface = surface
        self.MAX_W, self.MAX_H = self.surface.get_width(), self.surface.get_height()
        self.player = player

        self.DISP_W, self.DISP_H = display_width, display_height
        self.offset_from_player = pygame.math.Vector2(-self.DISP_W // 2,
                                                      -self.DISP_H // 2)
        self.offset = pygame.math.Vector2()
        self.offset.x = min(max(self.player.cur_rect.centerx - self.DISP_W // 2, 0), self.MAX_W - self.DISP_W)
        self.offset.y = min(max(self.player.cur_rect.centery - self.DISP_H // 2, 0), self.MAX_H - self.DISP_H)

    def scroll(self) -> tuple[int, int, int, int]:
        # print(self.MAX_W, self.MAX_H, self.player.cur_rect.centerx - self.DISP_W // 2, self.player.cur_rect.centery - self.DISP_H // 2, 0)
        self.offset.x = min(max(self.player.cur_rect.centerx - self.DISP_W // 2, 0), self.MAX_W - self.DISP_W)
        self.offset.y = min(max(self.player.cur_rect.centery - self.DISP_H // 2, 0), self.MAX_H - self.DISP_H)
        return (self.offset.x, self.offset.y, self.DISP_W, self.DISP_H)


    def set_surf(self, surface: pygame.Surface):
        self.surface = surface
        self.MAX_W, self.MAX_H = self.surface.get_width(), self.surface.get_height()

__author__ = 'Florian Tautz'

from pygame import Rect


class Camera:
    def __init__(self, view_size):
        self.view_rect = Rect((0, 0), view_size)

    def move(self, x, y):
        self.view_rect = self.view_rect.move(x, y)

    def rect_to_screen(self, rect):
        return rect.move(-self.view_rect.x, -self.view_rect.y)

    def point_to_screen(self, x, y):
        return x - self.view_rect.x, y - self.view_rect.y
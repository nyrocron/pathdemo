__author__ = 'Florian Tautz'

from pygame import Rect


class Camera:
    def __init__(self, view_size):
        self.rect = Rect((0, 0), view_size)

    def move(self, x, y):
        self.rect = self.rect.move(x, y)

    def get_offset(self):
        return -self.rect.x, -self.rect.y
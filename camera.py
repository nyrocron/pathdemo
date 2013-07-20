__author__ = 'Florian Tautz'

from pygame import Rect


class Camera:
    def __init__(self, view_size):
        self.rect = Rect((0, 0), view_size)

    def __getattr__(self, item):
        if item == 'offset':
            return self._pos_x, self._pos_y
        if item == 'view_rect':
            return Rect(self._pos_x, self._pos_y, self._width, self._height)

    def move(self, x, y):
        self._pos_x += x
        self._pos_y -= y
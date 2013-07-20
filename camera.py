__author__ = 'Florian Tautz'


class Camera:
    def __init__(self, view_size):
        self._width = view_size[0]
        self._height = view_size[1]
        self._pos_x = self._width / 2
        self._pos_y = self._height / 2

    def center_on(self, x, y):
        self._pos_x = self._width / 2 - x
        self._pos_y = self._height / 2 - y

    def move(self, x, y):
        self._pos_x += x
        self._pos_y -= y

    def get_view_rect(self):
        return (self._pos_x, self._pos_y,
                self._width, self._height)
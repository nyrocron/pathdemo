__author__ = 'Florian Tautz'

from pygame import image


class MapError(Exception):
    pass


class Map:
    _tile_size = 16

    def __init__(self, map_name=None):
        self._texmap = image.load('texmap.png')
        self._texmap_tiles_x = 16
        self._texmap_tiles_y = 16
        self._tiles = None
        if map_name is not None:
            self.load(map_name)

    def load(self, map_name):
        self.width = None
        self.Height = None
        self._tiles = []

        fh = open(map_name + '.map', 'r')
        for line in fh:
            items = [int(x) for x in line.split()]
            if self.width is None:
                self.width = len(items)
            else:
                if self.width != len(items):
                    raise MapError("line width does not match first line")
            self._tiles.append(items)
        fh.close()

        self.height = len(self._tiles)

    def get_center(self):
        x = self.width / 2 * self._tile_size
        y = self.height / 2 * self._tile_size
        return x, y

    def draw(self, surface, view_rect):
        """Draw part of the map

        :param surface: the surface to draw to
        :param view_rect: the part of the map to draw (x, y, width, height)
        """
        # TODO: culling

        for y in range(self.height):
            for x in range(self.width):
                src_rect = self._get_tex_rect(self._get_tile(x, y))
                dst_rect = (view_rect[0] + x * self._tile_size,
                            view_rect[1] + y * self._tile_size,
                            self._tile_size, self._tile_size)
                surface.blit(self._texmap, dst_rect, src_rect)

    def _get_tile(self, x, y):
        return self._tiles[y][x]

    def _get_tex_rect(self, texture_id):
        x = (texture_id % self._texmap_tiles_x) * self._tile_size
        y = (texture_id // self._texmap_tiles_x) * self._tile_size
        return x, y, self._tile_size, self._tile_size
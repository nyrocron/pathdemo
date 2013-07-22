# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""map.py: map background management"""

from pygame import image, Rect


class MapError(Exception):
    pass


class Map:
    """manages map background content and drawing"""

    MAP_DIR = 'content/maps/'
    _tile_size = 16

    def __init__(self, map_name=None):
        self.tiles_x = 0
        self.tiles_y = 0
        self.size = None
        self._texmap = image.load('content/texmap.png')
        self._texmap_tiles_x = 16
        self._texmap_tiles_y = 16
        self._tiles = None
        if map_name is not None:
            self.load(map_name)

    def load(self, map_name):
        """Load map with name map_name."""
        self.tiles_x = None
        self.tiles_y = None
        self._tiles = []

        fh = open(Map.MAP_DIR + map_name + '.map', 'r')
        for line in fh:
            items = [int(x) for x in line.split()]
            if self.tiles_x is None:
                self.tiles_x = len(items)
            else:
                if self.tiles_x != len(items):
                    raise MapError("line width does not match first line")
            self._tiles.append(items)
        fh.close()

        self.tiles_y = len(self._tiles)

        self.size = Rect(0, 0,
                         self.tiles_x * Map._tile_size,
                         self.tiles_y * Map._tile_size)

    def draw(self, surface, view_rect, to_screen):
        """Draw map to surface.

        Only draw tiles in view_rect and use to_screen to convert
        map coordinates to screen coordinates"""
        tile_startx = max(0, view_rect.x // Map._tile_size)
        tile_starty = max(0, view_rect.y // Map._tile_size)
        tiles_x = min(self.tiles_x - tile_startx,
                      view_rect.width // Map._tile_size)
        tiles_y = min(self.tiles_y - tile_starty,
                      view_rect.height // Map._tile_size)
        tile_size = (Map._tile_size, Map._tile_size)
        for y in range(tile_starty, tile_starty + tiles_y):
            for x in range(tile_startx, tile_startx + tiles_x):
                src_rect = self._get_tex_rect(self._get_tile(x, y))
                tile_pos = (x * Map._tile_size, y * Map._tile_size)
                dst_rect = Rect(to_screen(tile_pos), tile_size)
                surface.blit(self._texmap, dst_rect, src_rect)

    def _get_tile(self, x, y):
        return self._tiles[y][x]

    def _get_tex_rect(self, texture_id):
        x = (texture_id % self._texmap_tiles_x) * self._tile_size
        y = (texture_id // self._texmap_tiles_x) * self._tile_size
        return x, y, self._tile_size, self._tile_size
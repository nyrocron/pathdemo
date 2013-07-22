# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""rendering.py: handles rendering of the game"""

from pygame import image, draw


class Renderer:
    """Manages textures/assignments and provides methods for drawing objects
    and other graphics to pygame surfaces"""

    def __init__(self, surface, camera):
        self._surface = surface
        self._cam = camera
        self._textures = {}
        self._texture_assignments = {}

        unit_highlight_texture = self.load_texture('unit_highlight.png')
        self.assign_texture('unit_highlight', unit_highlight_texture)

    def load_texture(self, texture_name):
        """Load texture and return texture id."""
        tex = Texture(texture_name)
        self._textures[tex.id] = tex
        return tex.id

    def assign_texture(self, key, tex_id):
        """Assign texture to a key (for example object id)."""
        self._texture_assignments[key] = tex_id

    def texture_size(self, tex_id):
        """Get size of a texture by id."""
        return self._textures[tex_id].size

    def draw_map(self, map_):
        """Draw map at the appropriate location."""
        map_.draw(self._surface, self._cam.view_rect,
                  self._cam.point_to_screen)

    def draw_objects(self, objs):
        """Draw a set of objects at the appropriate location."""
        for obj in objs:
            self._draw_object(obj)
            if obj.selected:
                self._draw_highlight(obj.bbox)

    def draw_rectangle(self, rect, color, width=1):
        """Draw a simple non-filled rectangle."""
        draw.rect(self._surface, color, self._cam.rect_to_screen(rect), width)

    def _draw_object(self, obj):
        dst_rect = self._cam.rect_to_screen(obj.bbox)
        self._surface.blit(self._get_tex(obj.id), dst_rect)

    def _draw_highlight(self, rect):
        dst_rect = self._cam.rect_to_screen(rect)
        self._surface.blit(self._get_tex('unit_highlight'), dst_rect)

    def _get_tex(self, obj_id):
        tex_id = self._texture_assignments[obj_id]
        return self._textures[tex_id].surface


class TextureError(Exception):
    pass


class Texture:
    """Represents a texture"""
    TEXTURE_DIR = 'content/textures/'
    _id_counter = 0

    def __init__(self, texture_name):
        """Load texture with name texture_name."""
        texture_path = Texture.TEXTURE_DIR + texture_name
        try:
            self.surface = image.load(texture_path)
        except:
            raise TextureError("Error opening texture " + texture_path)
        self.size = self.width, self.height = self.surface.get_size()
        self.id = Texture._new_id()

    @staticmethod
    def _new_id():
        Texture._id_counter += 1
        return Texture._id_counter
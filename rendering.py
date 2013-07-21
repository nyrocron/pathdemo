__author__ = 'Florian Tautz'

from pygame import image, draw


class Renderer:
    def __init__(self, surface, camera):
        self._surface = surface
        self._cam = camera
        self._textures = {}
        self._texture_assignments = {}

        unit_highlight_texture = self.load_texture('unit_highlight.png')
        self.assign_texture('unit_highlight', unit_highlight_texture)

    def load_texture(self, texture_name):
        tex = Texture(texture_name)
        self._textures[tex.id] = tex
        return tex.id

    def assign_texture(self, key, tex_id):
        self._texture_assignments[key] = tex_id

    def texture_size(self, tex_id):
        return self._textures[tex_id].size

    def draw_map(self, map_):
        map_.draw(self._surface, self._cam.view_rect,
                  self._cam.point_to_screen)

    def draw_objects(self, objs):
        for obj in objs:
            self._draw_object(obj)
            if obj.selected:
                self._draw_highlight(obj.bbox)

    def draw_rectangle(self, rect, color):
        draw.rect(self._surface, color, self._cam.rect_to_screen(rect), 1)

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
    TEXTURE_DIR = 'content/textures/'
    _id_counter = 0

    def __init__(self, texture_name):
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
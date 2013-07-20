__author__ = 'Florian Tautz'

from pygame import image


class Renderer:
    def __init__(self, surface, camera):
        self._surface = surface
        self._cam = camera
        self._textures = {}
        self._texture_assignments = {}

    def load_texture(self, texture_name):
        tex = Texture(texture_name)
        self._textures[tex.id] = tex
        return tex.id

    def assign_texture(self, obj_id, tex_id):
        self._texture_assignments[obj_id] = tex_id

    def texture_size(self, tex_id):
        return self._textures[tex_id].size

    def draw_map(self, map_):
        map_.draw(self._surface, self._cam.view_rect,
                  self._cam.point_to_screen)

    def _draw_map_tile(self, tile):
        pass

    def draw_objects(self, objs):
        for obj in objs:
            self._draw_object(obj)

    def _draw_object(self, obj):
        dst_rect = self._cam.rect_to_screen(obj.bbox)
        self._surface.blit(self._get_tex(obj.id), dst_rect)

    def _get_tex(self, obj_id):
        tex_id = self._texture_assignments[obj_id]
        return self._textures[tex_id].surface


class Texture:
    TEXTURE_DIR = 'content/textures/'
    _id_counter = 0

    def __init__(self, texture_name):
        self.surface = image.load(Texture.TEXTURE_DIR + texture_name)
        self.size = self.width, self.height = self.surface.get_size()
        self.id = Texture._new_id()

    @staticmethod
    def _new_id():
        Texture._id_counter += 1
        return Texture._id_counter
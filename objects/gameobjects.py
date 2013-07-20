__author__ = 'Florian Tautz'


class GameObject:
    _id_counter = 0

    def __init__(self, bbox, obj_id=None):
        self.bbox = bbox
        if obj_id is None:
            self.id = GameObject._new_id()
        else:
            self.id = obj_id

    def __repr__(self):
        return '<' + str(self) + '>'

    def __str__(self):
        return ('GameObject(' + str(self.bbox) + ', id=' + str(self.id) + ')')

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other

    def __getattr__(self, item):
        if item == 'size':
            return self.bbox.width, self.bbox.height

    @staticmethod
    def _new_id():
        GameObject._id_counter += 1
        return GameObject._id_counter


class Unit(GameObject):
    pass
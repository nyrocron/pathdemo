__author__ = 'flori_000'

from geometry import Rectangle
from objects.management import Quadtree


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
        return self.id == other.id

    @staticmethod
    def _new_id():
        GameObject._id_counter += 1
        return GameObject._id_counter

if __name__ == '__main__':
    q = Quadtree(Rectangle(0, 0, 16, 16))

    objs = [GameObject(Rectangle(0, 0, 1, 1)),
            GameObject(Rectangle(1, 1, 1, 1)),
            GameObject(Rectangle(2, 4, 1, 1)),
            GameObject(Rectangle(4, 2, 1, 1)),
            GameObject(Rectangle(1, 1, 8, 8)),
            GameObject(Rectangle(3, 8, 2, 4))]

    for obj in objs:
        q.insert(obj)

    q.print_tree()
    print(q.query_intersect(Rectangle(1.1, 1.1, 4, 4)))
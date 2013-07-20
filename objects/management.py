__author__ = 'Florian Tautz'

from pygame import Rect


class TreeError(Exception):
    pass


class QuadtreeNode:
    MAX_ITEMS = 6

    def __init__(self, parent, bbox):
        if (not self._is_power2(bbox.width) or
            not self._is_power2(bbox.height)):
            raise TreeError("node dimensions have to be power of two,"
                            " bbox given was " + str(bbox))

        self.parent = parent
        self._bb = bbox

        self._data = set()
        self._has_children = False
        self._childs = [None] * 4

    def insert(self, obj):
        if not self._bb.contains(obj.bbox):
            return False

        if not self._has_children:
            self._subdivide()

        if self._has_children:
            for child in self._childs:
                if child.insert(obj):
                    return True

        self._data.add(obj)
        return True

    def query(self, area=None):
        result = set()
        if area is not None and not self._bb.contains_rect(area):
            return result

        if len(self._data) > 0:
            for obj in self._data:
                if area is None or area.contains_rect(obj.bbox):
                    result.add(obj)

        if not self._has_children:
            return result

        for child in self._childs:
            result.update(child.query(area))

        return result

    def query_intersect(self, area):
        result = set()
        if not self._bb.colliderect(area):
            return result

        if len(self._data) > 0:
            for obj in self._data:
                if obj.bbox.colliderect(area):
                    result.add(obj)

        if not self._has_children:
            return result

        for child in self._childs:
            result.update(child.query_intersect(area))

        return result

    def move_to(self, obj, new_bbox):
        if not self._bb.contains(obj.bbox):
            return False
        if self._bb.contains(obj.bbox) and obj in self._data:
            self._data.remove(obj)
            self._purge_empty_nodes()
            obj.bbox = new_bbox
            self.insert_up(obj)
            return True
        for child in self._childs:
            if child.move_to(obj, new_bbox):
                return True
        raise TreeError("move failed")

    def insert_up(self, obj):
        if self._bb.contains(obj.bbox):
            self.insert(obj)
        else:
            self.parent.insert_up(obj)

    def print_tree(self, indent=0):
        print(' ' * indent + str(self._data))

        if not self._has_children:
            return

        for child in self._childs:
            child.print_tree(indent + 2)

    def _subdivide(self):
        split_width = self._bb.width // 2
        split_height = self._bb.height // 2
        split_x = self._bb.x + split_width
        split_y = self._bb.y + split_height

        if split_width == 0 or split_height == 0:
            return False

        self._childs[0] = QuadtreeNode(self, Rect(self._bb.x, self._bb.y,
                                                  split_width, split_height))
        self._childs[1] = QuadtreeNode(self, Rect(split_x, self._bb.y,
                                                  split_width, split_height))
        self._childs[2] = QuadtreeNode(self, Rect(self._bb.x, split_y,
                                                  split_width, split_height))
        self._childs[3] = QuadtreeNode(self, Rect(split_x, split_y,
                                                  split_width, split_height))

        self._has_children = True
        return True

    def _has_data(self):
        return len(self._data) > 0

    def _purge_empty_nodes(self):
        if self._has_data():
            return

        if self._has_children:
            for child in self._childs:
                if child._has_children or child._has_data():
                    return

        self._childs = [None] * 4
        self._has_children = False
        if self.parent is not None:
            self.parent._purge_empty_nodes()

    def _is_power2(self, n):
        return ((n & (n - 1)) == 0) and n > 0


class Quadtree(QuadtreeNode):
    def __init__(self, bbox):
        super(Quadtree, self).__init__(None, bbox)


class ObjectManagementError(Exception):
    pass


class ObjectManager:
    def __init__(self, bbox):
        self._bb = bbox
        self._quadtree = Quadtree(self._bb)
        self._id_to_obj = {}

    def create(self, which, location):
        obj = which(location)
        self._id_to_obj[obj.id] = obj
        self._quadtree.insert(obj)
        return obj

    def query(self, area=None):
        if area is None:
            area = self._bb
        return self._quadtree.query_intersect(area)

    def get_object_by_id(self, obj_id):
        return self._id_to_obj[obj_id]

    def move_object(self, obj_id, x, y):
        obj = self.get_object_by_id(obj_id)
        new_bbox = obj.bbox.move(x, y)
        if not self._bb.contains(new_bbox):
            return False
        self._quadtree.move_to(obj, new_bbox)
        return True
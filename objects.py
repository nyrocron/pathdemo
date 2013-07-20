__author__ = 'Florian Tautz'


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_center(self):
        return self.x + self.width // 2, self.y + self.height // 2

    def contains(self, x, y):
        return (x >= self.x and y >= self.y and
                x <= self.x + self.width and
                y <= self.y + self.height)
    
    def intersects(self, other):
        separate = (self.x + self.width < other.x or
                    self.y + self.height < other.y or
                    self.x > other.x + other.width or
                    self.y > other.y + other.height)
        return not separate
    

class TreeError(Exception):
    pass


class QuadtreeNode:
    MAX_ITEMS = 6
    
    def __init__(self, parent, bbox):
        if (not self._is_power2(bbox.width) or
            not self._is_power2(bbox.height)):
            raise TreeError("node dimensions have to be power of two")
        
        self.parent = parent
        self._bb = bbox
        
        self._data = []
        self._has_children = False
        self._childs = [None] * 4

    def insert(self, obj):
        if not obj.in_rect(self._bb):
            return False
        
        if len(self._data) < self.MAX_ITEMS:
            self._data = [obj]
            return True
        
        if not self._has_children:
            self._subdivide()
        
        for child in self._childs:
            if child.insert(obj):
                return True
        
        raise TreeError("insertion failed somehow. this should not happen")

    def query(self, area=None):
        result = set()
        if area is not None and not self._bb.intersects(area):
            return result
        
        if len(self._data) > 0:
            for obj in self._data:
                if area is None or obj.in_rect(area):
                    result.add(obj)
        
        if not self._has_children:
            return result
        
        for child in self._childs:
            result.update(child.query(area))
        
        return result
    
    def _subdivide(self):
        split_width = self._bb.width // 2
        split_height = self._bb.height // 2
        split_x = self._bb.x + split_width
        split_y = self._bb.y + split_height
        
        self._childs[0] = QuadtreeNode(self,
                                       Rectangle(self._bb.x,
                                                 self._bb.y,
                                                 split_width,
                                                 split_height))
        self._childs[1] = QuadtreeNode(self,
                                       Rectangle(split_x,
                                                 self._bb.y,
                                                 split_width,
                                                 split_height))
        self._childs[2] = QuadtreeNode(self,
                                       Rectangle(self._bb.x,
                                                 split_y,
                                                 split_width,
                                                 split_height))
        self._childs[3] = QuadtreeNode(self,
                                       Rectangle(split_x,
                                                 split_y,
                                                 split_width,
                                                 split_height))

        self._has_children = True
    
    def _is_power2(self, n):
        return ((n & (n - 1)) == 0) and n > 0


class Quadtree(QuadtreeNode):
    def __init__(self, bbox):
        super(Quadtree, self).__init__(None, bbox)


class ObjectManager:
    def __init__(self, bounds):
        self._id_counter = -1
        self._id_to_object = []
        self._ids = Quadtree(bounds)
    
    def create(self, what, x, y):
        obj = what(x, y)
        obj_id = self._get_id()
        self._id_to_object.append((obj_id, obj))
        self._ids.insert(x, y, obj_id)
        return obj
    
    def query(self, area=None):
        obj_ids = self._ids.query(area)
        return [self._get_obj(obj_id) for obj_id in obj_ids]
    
    def _get_obj(self, obj_id):
        min_index = 0
        max_index = len(self._id_to_object) - 1
        while True:
            current_index = min_index + (max_index - min_index) // 2
            current_id, current_obj = self._id_to_object[current_index]
            if current_id == obj_id:
                return current_obj
            if obj_id < current_id:
                max_index = current_index - 1
                continue
            if obj_id > current_id:
                min_index = current_index + 1
                continue
    
    def _get_id(self):
        self._id_counter += 1
        return self._id_counter
    
class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return 'GameObject' + str(self)
    
    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'
    
    def in_rect(self, rect):
        return rect.contains(self.x, self.y)
    
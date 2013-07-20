__author__ = 'Florian Tautz'


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.right = self.x + self.width
        self.bottom = self.y + self.height

    def __str__(self):
        return ('Rectangle(' + str(self.x) + ', ' + str(self.y) + ', ' +
                str(self.width) + ', ' + str(self.height) + ')')

    def get_center(self):
        return self.x + self.width // 2, self.y + self.height // 2

    def contains_point(self, x, y):
        return (x >= self.x and y >= self.y and
                x <= self.x + self.width and
                y <= self.y + self.height)

    def contains_rect(self, other):
        return (other.x >= self.x and other.right <= self.right and
                other.y >= self.y and other.bottom <= self.bottom)
    
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
            raise TreeError("node dimensions have to be power of two,"
                            " bbox given was " + str(bbox))
        
        self.parent = parent
        self._bb = bbox
        
        self._data = set()
        self._has_children = False
        self._childs = [None] * 4

    def insert(self, obj):
        if not self._bb.contains_rect(obj.bbox):
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
        if not self._bb.intersects(area):
            return result
        
        if len(self._data) > 0:
            for obj in self._data:
                if obj.bbox.intersects(area):
                    result.add(obj)
        
        if not self._has_children:
            return result
        
        for child in self._childs:
            result.update(child.query_intersect(area))
        
        return result    
    
    def move(self, obj, new_bbox):
        if not self._bb.contains_rect(obj.bbox):
            return False
        if self._bb.contains_rect(obj.bbox) and obj in self._data:
            self._data.remove(obj)
            self._purge_empty_nodes()
            obj.bbox = new_bbox
            self.insert_up(obj)
            return True
        for child in self._childs:
            if child.move(obj, new_bbox):
                return True
        raise TreeError("move failed")

    def insert_up(self, obj):
        if self._bb.contains_rect(obj.bbox):
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
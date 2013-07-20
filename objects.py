__author__ = 'Florian Tautz'


class ObjectManager:
    def __init__(self):
        self._objects = QuadtreeNode()
    
    def create(self, type):
        
        pass
    
    
    def get_in_area(self, area):
        return self._objects.query(area)
    

class TreeError(Exception):
    pass


class QuadtreeNode:
    def __init__(self, bounds):
        if (not self._is_power2(bounds.width) or
            not self._is_power2(bounds.height)):
            raise TreeError("node dimensions have to be power of two")
        
        self._bounds = bounds
        
        self._data = None
        self._has_children = False
        self._childs = [None] * 4

    def insert(self, x, y, data):
        if not self._bounds.contains(x, y):
            return False
        
        if self._data is None:
            self._data = (x, y, data)
            return True
        
        if not self._has_children:
            self._subdivide()
        
        for child in self._childs:
            if child.insert(x, y, data):
                return True
        
        raise TreeError("insertion failed somehow. this should not happen")

    def query(self, area=None):
        result = []
        if area is not None and not self._bounds.intersects(area):
            return result
        
        if self._data is not None:
            if area is None or area.contains(self._data[0], self._data[1]):
                result.append(self._data[2])
        
        if not self._has_children:
            return result
        
        for child in self._childs:
            result += child.query(area)
        
        return result
    
    def _subdivide(self):
        split_width = self._bounds.width // 2
        split_height = self._bounds.height // 2
        split_x = self._bounds.x + split_width
        split_y = self._bounds.y + split_height
        
        self._childs[0] = QuadtreeNode(Rectangle(self._bounds.x,
                                                 self._bounds.y,
                                                 split_width,
                                                 split_height))
        self._childs[1] = QuadtreeNode(Rectangle(split_x,
                                                 self._bounds.y,
                                                 split_width,
                                                 split_height))
        self._childs[2] = QuadtreeNode(Rectangle(self._bounds.x,
                                                 split_y,
                                                 split_width,
                                                 split_height))
        self._childs[3] = QuadtreeNode(Rectangle(split_x,
                                                 split_y,
                                                 split_width,
                                                 split_height))
        
        self._has_children = True
    
    def _is_power2(self, n):
        return ((n & (n - 1)) == 0) and n > 0


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
    
# encoding: utf-8


from math import sqrt


class Vector3:
    __slots__ = 'x', 'y', 'z', 'triangles', 'neighbors', 'collapse_neighbor', 'collapse_cost'

    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z
        self.triangles = []
        self.neighbors = []
        self.collapse_neighbor = None
        self.collapse_cost = None

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z = other.z
        return sqrt(dx * dx + dy * dy + dz * dz)

    def add_neighbors(self, vertices):
        for vertex in vertices:
            self.add_neighbor(vertex)

    def add_neighbor(self, vertex):
        if vertex not in self.neighbors and vertex != self:
            self.neighbors.append(vertex)
            vertex.neighbors.append(self)

    def remove_neighbor(self, vertex):
        if vertex not in self.neighbors:
            return

        for triangle in self.triangles:
            if triangle.has_vertex(vertex):
                return

        self.neighbors.remove(vertex)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __repr__(self):
        return '(%s, %s, %s)' % (self.x, self.y, self.z)

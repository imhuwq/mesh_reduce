# encoding: utf-8


from math import sqrt


class Vector3(object):
    __slots__ = 'x', 'y', 'z', 'triangles', 'neighbors', 'collapse_neighbor', 'collapse_cost', 'normal', 'tex_coord0'

    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z
        self.triangles = []
        self.neighbors = []
        self.collapse_neighbor = None
        self.collapse_cost = None

        self.normal = None
        self.tex_coord0 = None

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return sqrt(dx * dx + dy * dy + dz * dz)

    def add_triangle(self, triangle):
        if triangle not in self.triangles:
            self.triangles.append(triangle)
        for vertex in triangle.vertices:
            self.add_neighbor(vertex)

    def remove_triangle(self, triangle):
        if triangle not in self.triangles:
            return
        self.triangles.remove(triangle)
        for vertex in triangle.vertices:
            self.remove_neighbor(vertex)

    def add_neighbors(self, vertices):
        for vertex in vertices:
            self.add_neighbor(vertex)

    def add_neighbor(self, vertex):
        if vertex != self:
            if vertex not in self.neighbors:
                self.neighbors.append(vertex)
            if self not in vertex.neighbors:
                vertex.neighbors.append(self)

    def remove_neighbor(self, vertex):
        if vertex not in self.neighbors:
            return
        for triangle in self.triangles:
            if triangle.has_vertex(vertex):
                return
        self.neighbors.remove(vertex)
        try:
            vertex.neighbors.remove(self)
        except ValueError:
            pass

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and \
               self.normal == other.normal and self.tex_coord0 == other.tex_coord0

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __repr__(self):
        return '(%s, %s, %s)' % (self.x, self.y, self.z)

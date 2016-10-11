# encoding: utf-8


from .vector3 import Vector3


class Triangle(object):
    __slots__ = 'normal', 'vertices'

    def __init__(self):
        self.normal = Vector3()
        self.vertices = []

    def add_vertex(self, vertex):
        self.vertices.append(vertex)
        vertex.add_triangle(self)

    def has_vertex(self, vertex):
        return vertex in self.vertices

    def remove_vertex(self, vertex):
        if vertex not in self.vertices:
            return
        self.vertices.remove(vertex)
        vertex.remove_triangle(self)

    def replace_vertex(self, old, new):

        index = self.vertices.index(old)
        self.vertices[index] = new

        self.remove_vertex(old)
        old.remove_triangle(self)
        new.add_triangle(self)

        self.compute_normal()

    def compute_normal(self):
        p1, p2, p3 = self.vertices
        u = p2 - p1
        v = p3 - p1
        self.normal.x = (u.y * v.z) - (u.z * v.y)
        self.normal.y = (u.z * v.x) - (u.x * v.z)
        self.normal.z = (u.x * v.y) - (u.y * v.x)

    @property
    def is_a_line(self):
        p1, p2, p3 = self.vertices
        sides = sorted([p1.distance_to(p2), p1.distance_to(p3), p2.distance_to(p3)])
        return sides[2] == sides[0] + sides[1]

    def __repr__(self):
        return '<Vertices: p1%s, p2%s, p3%s>\n' \
               % (self.vertices[0], self.vertices[1], self.vertices[2])

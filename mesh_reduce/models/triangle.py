# encoding: utf-8


from .vector3 import Vector3


class Triangle:
    __slots__ = 'normal', 'vertices'

    def __init__(self):
        self.normal = Vector3()
        self.vertices = []

    def add_vertex(self, vertex):
        self.vertices.append(vertex)
        for vertex in self.vertices:
            vertex.add_neighbors(self.vertices)
        vertex.triangles.append(self)

    def has_vertex(self, vertex):
        return vertex in self.vertices

    def remove_vertex(self, vertex):
        try:
            self.vertices.remove(vertex)
        except ValueError:
            return

    def replace_vertex(self, old, new):
        index = self.vertices.index(old)
        self.vertices[index] = new
        p1, p2, p3 = self.vertices

        old.triangles.remove(self)
        new.triangles.append(self)

        old.remove_neighbor(p1)
        p1.remove_neighbor(old)

        old.remove_neighbor(p2)
        p2.remove_neighbor(old)

        old.remove_neighbor(p3)
        p3.remove_neighbor(old)

        p1.add_neighbor(p2)
        p1.add_neighbor(p3)

        p2.add_neighbor(p1)
        p2.add_neighbor(p3)

        p3.add_neighbor(p1)
        p3.add_neighbor(p2)

        self.compute_normal()

    def compute_normal(self):
        p1, p2, p3 = self.vertices
        u = p2 - p1
        v = p3 - p1
        self.normal.x = (u.y * v.z) - (u.z * v.y)
        self.normal.y = (u.z * v.x) - (u.x * v.z)
        self.normal.z = (u.x * v.y) - (u.y * v.x)

    def __repr__(self):
        return 'Triangle Object: \n <Vertices: p1%s, p2%s, p3%s>, \n <Normal: %s>\n' \
               % (self.vertices[0], self.vertices[1], self.vertices[2], self.normal)

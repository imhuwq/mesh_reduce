# encoding: utf-8


class Mesh:
    __slots__ = 'name', 'triangles', 'vertices'

    def __init__(self, name=None):
        self.name = name
        self.triangles = list()
        self.vertices = list()

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def remove_vertex(self, vertex):
        self.vertices.remove(vertex)
        for neighbor in vertex.neighbors:
            neighbor.remove_neighbor(vertex)

    def add_triangle(self, triangle):
        self.triangles.append(triangle)

    def remove_triangle(self, triangle):
        try:
            self.triangles.remove(triangle)
            for vertex in triangle.vertices:
                if vertex:
                    vertex.triangles.remove(triangle)

            for i in range(len(triangle.vertices)):
                v1 = triangle.vertices[i]
                v2 = triangle.vertices[(i + 1) % 3]

                if not v1 or not v2:
                    continue

                v1.remove_neighbor(v2)
                v2.remove_neighbor(v1)
        except ValueError:
            return

    def compute_uv_cost(self, u, v):

        tu = u.triangles  # triangles_has_u
        tuv = [triangle for triangle in u.triangles if triangle in v.triangles]  # triangles_has_uv

        distance = v.distance_to(u)

        max_cost = 0
        for u_face in tu:
            min_cost = 1  # min_cost 最终必定会小于 1
            for uv_face in tuv:
                cost = (1 - u_face.normal.dot(uv_face.normal)) / 2
                min_cost = min(min_cost, cost)
            max_cost = max(max_cost, min_cost)

        return distance * max_cost

    def compute_vertex_cost(self, vertex):
        if not vertex.neighbors:
            return

        min_cost = 0
        total_cost = 0
        cost_count = 0
        for neighbor in vertex.neighbors:
            collapse_cost = self.compute_uv_cost(vertex, neighbor)

            if not min_cost:
                vertex.collapse_neighbor = neighbor
                min_cost = collapse_cost

            cost_count += 1
            total_cost += collapse_cost

            if collapse_cost < min_cost:
                min_cost = collapse_cost
                vertex.collapse_neighbor = neighbor

        vertex.collapse_cost = total_cost / cost_count
        return vertex.collapse_cost

    def collapse(self, vertex):
        u = vertex
        v = vertex.collapse_neighbor
        if u and not v:
            self.remove_vertex(u)
            return

        tmp_neighbors = u.neighbors[:]

        for triangle in u.triangles:
            if triangle.has_vertex(v):
                self.remove_triangle(triangle)

        for triangle in u.triangles:
            triangle.replace_vertex(u, v)

        self.remove_vertex(u)

        for vertex in tmp_neighbors:
            self.compute_vertex_cost(vertex)

    def get_vertex_of_minimum_cost(self):
        vertex = self.vertices[0]
        min_cost = vertex.collapse_cost

        for v in self.vertices:
            if v.collapse_cost is not None and v.collapse_cost < min_cost:
                vertex = v
        return vertex

    def reduce_vertex(self, count):
        max_count = len(self.vertices) - 1
        count = min(count, max_count)

        print(self)
        collapsed_count = 0

        for vertex in self.vertices:
            if not vertex.neighbors:
                self.remove_vertex(vertex)
                collapsed_count += 1
                continue
            self.compute_vertex_cost(vertex)

        print(collapsed_count)
        vertex = self.get_vertex_of_minimum_cost()

        while collapsed_count < count:
            collapsed_count += 1
            self.collapse(vertex)
            print(collapsed_count)

            vertex = self.get_vertex_of_minimum_cost()
        print(self)

    def __repr__(self):
        return "Mesh <%s> with %d vertices and %d triangles" \
               % (self.name, len(self.vertices), len(self.triangles))

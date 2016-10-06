# encoding: utf-8


class Mesh(object):
    __slots__ = 'name', 'index', 'vertices_index', 'triangles', 'vertices', 'bug'

    def __init__(self, name=None, index=None, vertices_index=None):
        self.name = name
        self.index = index
        self.vertices_index = vertices_index
        self.triangles = list()
        self.vertices = list()

        self.bug = 0

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def remove_vertex(self, vertex):
        self.vertices.remove(vertex)
        for neighbor in vertex.neighbors[:]:
            neighbor.remove_neighbor(vertex)

    def add_triangle(self, triangle):
        self.triangles.append(triangle)

    def remove_triangle(self, triangle):
        if triangle not in self.triangles:
            return

        self.triangles.remove(triangle)
        for vertex in triangle.vertices:
            vertex.remove_triangle(triangle)

        for i in range(len(triangle.vertices)):
            v1 = triangle.vertices[i]
            v2 = triangle.vertices[(i + 1) % 3]

            if not v1 or not v2:
                continue

            v1.remove_neighbor(v2)

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
            vertex.collapse_neighbor = None
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

        # TODO: 为什么会出现v 不在面上的情况? PlayCanvas 的输出包含了重复的点!
        # if v not in self.vertices:
        #     raise BaseException('\n%s is collapsing to %s, but target is not on the mesh\n' % (u, v))

        neighbors = u.neighbors[:]

        for triangle in u.triangles[:]:
            if triangle.has_vertex(v):
                self.remove_triangle(triangle)
                if v and v.x == -17.1312 and v.y == 81.553 and v.z == -23.5315 and u.x == -17.6045 and u.y == 83.6304 and u.z == -23.5315:
                    print('  removed the triangle')
            else:
                triangle.replace_vertex(u, v)

        self.remove_vertex(u)

        for vertex in neighbors:
            self.compute_vertex_cost(vertex)

    def get_vertex_of_minimum_cost(self):
        vertex = self.vertices[0]
        min_cost = vertex.collapse_cost

        for v in self.vertices:
            if v.collapse_cost is not None and v.collapse_cost < min_cost:
                vertex = v
        return vertex

    def reduce_vertex(self, degree):
        print(self)
        count = min(int(len(self.vertices) * degree), len(self.vertices) - 1)
        collapsed_count = 0

        for vertex in self.vertices:
            if not vertex.neighbors and collapsed_count < count:
                self.remove_vertex(vertex)
                collapsed_count += 1
                continue

            self.compute_vertex_cost(vertex)

        vertex = self.get_vertex_of_minimum_cost()

        while collapsed_count < count:
            collapsed_count += 1
            self.collapse(vertex)
            vertex = self.get_vertex_of_minimum_cost()
        print(self)

    def jsonify(self):

        pos_data = []
        tex_data = []
        nor_data = []

        aabb_max = None
        aabb_min = None

        for vertex in self.vertices:
            x, y, z = vertex.x, vertex.y, vertex.z
            pos_data.extend([x, y, z])
            tex_data.extend(vertex.tex_coord0)
            nor_data.extend(vertex.normal)

            if not aabb_max:
                aabb_max = [x, y, z]
            else:
                aabb_max = map(max, zip(aabb_max, [x, y, z]))
            if not aabb_min:
                aabb_min = [x, y, z]
            else:
                aabb_min = map(min, zip(aabb_min, [x, y, z]))

        vertices_json_data = {
            'position': {'type': 'float32', 'data': pos_data, 'components': 3},
            'texCoord0': {'type': 'float32', 'data': tex_data, 'components': 2},
            'normal': {'type': 'float32', 'data': nor_data, 'components': 3},
        }

        indices = []
        for triangle in self.triangles:
            for vertex in triangle.vertices:
                indices.append(self.vertices.index(vertex))

        mesh_json_data = {
            "count": len(self.triangles) * 3,
            "aabb": {
                "max": aabb_max,
                "min": aabb_min
            },
            "vertices": self.vertices_index,
            "base": 0,
            "indices": indices,
            "type": "triangles"
        }

        return mesh_json_data, vertices_json_data

    def __repr__(self):
        return "Mesh <%s> with %d vertices and %d triangles" \
               % (self.name, len(self.vertices), len(self.triangles))

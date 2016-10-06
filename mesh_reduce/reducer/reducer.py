# encoding: utf-8

import json

from ..models import Vector3, Triangle, Mesh


class Reducer(object):
    def __init__(self, file_path, target_mesh_indices, degree, output=None):
        self.file_path = file_path
        self.file_name = file_path.split('/')[-1].rsplit('.', 1)[0]
        self.target_mesh_indices = target_mesh_indices
        self.degree = degree
        if not output:
            output = 'sample_data/' + self.file_name + '_reduced_[' + \
                     ','.join(map(str, self.target_mesh_indices)) + \
                     ']_by_' + str(self.degree) + '.json'
        self.output = output

        self.meshes = []
        self.original_data = None
        self.load_data()

    def load_data(self):

        with open(self.file_path, 'r') as f:
            data = json.load(f).get('model')

        self.original_data = data

        meshes = data.get('meshes')
        nodes = data.get('nodes')
        mesh_instances = data.get('meshInstances')

        for mesh_instance in mesh_instances:

            # 只读取目标 mesh
            mesh_index = mesh_instance.get('mesh')
            if mesh_index not in self.target_mesh_indices:
                continue

            mesh_name = nodes[mesh_instance.get('node')].get('name')

            mesh_data = meshes[mesh_index]
            vertices_index = mesh_data.get('vertices')

            mesh_object = Mesh(mesh_name, mesh_index, vertices_index)

            # 获取所有的顶点的数据, 三个一组成一个顶点
            vertices_data = data.get('vertices')[vertices_index]
            pos_data = vertices_data.get('position').get('data')
            tex_data = vertices_data.get('texCoord0').get('data')
            nor_data = vertices_data.get('normal').get('data')
            # 获取 mesh 对象的 vertices
            for i in range(0, len(pos_data), 3):
                vertex = Vector3(*map(float, pos_data[i:i + 3]))
                vertex.normal = nor_data[i:i + 3]
                tex_index = (i / 3) * 2
                vertex.tex_coord0 = tex_data[tex_index:tex_index + 2]
                mesh_object.add_vertex(vertex)

            # 获取 mesh 对象的 triangles
            indices = mesh_data.get('indices')
            for i in range(0, len(indices), 3):
                vertex_indices = indices[i], indices[i + 1], indices[i + 2]  # 三个顶点的 index
                triangle = Triangle()

                # 获取三个顶点
                for vertex_index in vertex_indices:
                    vertex = mesh_object.vertices[vertex_index]
                    triangle.add_vertex(vertex)

                triangle.compute_normal()

                mesh_object.add_triangle(triangle)

            self.meshes.append(mesh_object)

    def reduce_meshes(self):
        for mesh in self.meshes:
            mesh.reduce_vertex(self.degree)

    def dump_data(self):
        for mesh in self.meshes:
            mesh_index = mesh.index
            vertices_index = mesh.vertices_index
            mesh_data, vertices_data = mesh.jsonify()
            self.original_data.get('meshes')[mesh_index] = mesh_data
            self.original_data.get('vertices')[vertices_index] = vertices_data

        output_data = {'model': self.original_data}

        with open(self.output, 'w') as f:
            json.dump(output_data, f)

# encoding: utf-8

import json

from .models import Mesh, Triangle, Vector3


def load_json(data_path=None):
    if not data_path:
        raise BaseException('Please pass in the file path of your json file')

    with open(data_path, 'r') as f:
        data = json.load(f).get('model')
    mesh_objects = []

    meshes = data.get('meshes')
    nodes = data.get('nodes')
    mesh_instances = data.get('meshInstances')

    for mesh_instance in mesh_instances:

        # 获取 mesh 名称, 创建 mesh 对象
        mesh_name = nodes[mesh_instance.get('node')].get('name')
        mesh_object = Mesh(mesh_name)

        mesh_data = meshes[mesh_instance.get('mesh')]

        # 获取所有的顶点的数据, 三个一组成一个顶点
        pos_data = data.get('vertices')[mesh_data.get('vertices')].get('position').get('data')
        # 获取 mesh 对象的 vertices
        for i in range(0, len(pos_data), 3):
            mesh_object.add_vertex(Vector3(*pos_data[i:i + 3]))

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

        mesh_objects.append(mesh_object)

    return mesh_objects

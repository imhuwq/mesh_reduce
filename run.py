from mesh_reduce import load_json

mesh = load_json('sample_data/chair.json')[1]

mesh.reduce_vertex(1000)

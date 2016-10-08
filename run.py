from mesh_reduce import Reducer

reducer = Reducer('sample_data/chair.json', [0, 1, 2], 0.5)


reducer.reduce_meshes()
reducer.dump_data()

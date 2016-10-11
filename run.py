from mesh_reduce import Reducer

reducer = Reducer('sample_data/chair.json', [1], 0.5,
                  output='/home/john/sites/sofa/files/assets/4465425/1/sofa.json')


reducer.reduce_meshes()
reducer.dump_data()

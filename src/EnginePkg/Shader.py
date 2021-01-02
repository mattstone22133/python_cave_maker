from OpenGL import *

class Shader(GpuResource):
    def __init__(self, 
    vertex_src:String=None,
    fragment_src:String=None,
    geometry_src:String=None):
        ''' shaders are constructed when opengl resources are available. Prefer sharing shader objects, instead of recreating them 
        as shaders are gpu resources and duplicating them is unnecssary, wasteful, and slow.  .'''
        self.vertex_src = vertex_src
        self.fragment_src = fragment_src
        self.geometry_src = geometry_src
        super().__init__()

    def acquire_resources_v(self):
        super().acquire_resources_v()
        #todo build shaders
    
    def release_resources_v(self):
        super().release_resources_v()
        #todo tear down shaders

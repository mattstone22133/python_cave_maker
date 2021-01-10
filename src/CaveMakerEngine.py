from OpenGL.GL import *
from EnginePkg.Engine import Engine
from EnginePkg.Shader import Shader
from GamePkg.Cube import Cube
from GamePkg.SharedShaders import WorldCubeShader_vs, WorldCubeShader_fs #TODO move this to a better location after initial testing

class CaveMakerEngine(Engine):
    def __init__(self) -> None:
        super().__init__()
        #temp
        self.cube = None #TODO must wait on opengl resources

    def create_window_v(self):
        ret = super().create_window_v()

        #TODO move this, temp code to get things working
        self.cube = Cube()
        self.cube_shader = Shader(vertex_src=WorldCubeShader_vs, fragment_src=WorldCubeShader_fs)

        return ret;
    
    def render_v(self, delta_sec: float):
        ''' note: add temporary testing code for initial engine iteration here, but do not check it in. '''
        super().render_v(delta_sec)
        glClearColor(1,0,0,0) 
        glClear(GL_COLOR_BUFFER_BIT)

        if self.cube is not None and self.cube_shader is not None:
            self.cube_shader.use()
            self.cube.render()

    
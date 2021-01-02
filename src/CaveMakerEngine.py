import OpenGL.GL as gl
from EnginePkg.Engine import Engine
from GamePkg.Cube import Cube

class CaveMakerEngine(Engine):
    def __init__(self) -> None:
        super().__init__()
        #temp
        self.cube = None #TODO must wait on opengl resources

    def create_window_v(self):
        ret = super().create_window_v()
        self.cube = Cube() #TODO do this in init, and let events drive OpenGL resource acquistion

        return ret;
    
    def render_v(self, delta_sec: float):
        super().render_v(delta_sec)
        gl.glClearColor(1,0,0,0) 
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        if self.cube is not None:
            self.cube.render()

    
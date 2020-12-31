import OpenGL.GL as gl
from EnginePkg.Engine import Engine

class CaveMakerEngine(Engine):
    def __init__(self) -> None:
        super().__init__()

    def create_window_v(self):
        return super().create_window_v()
    
    def render_v(self, delta_sec: float):
        super().render_v(delta_sec)
        gl.glClearColor(1,0,0,0) 
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    
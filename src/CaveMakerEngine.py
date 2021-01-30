from OpenGL.GL import *
from EnginePkg.Camera import CameraBase
from EnginePkg.Engine import Engine
from EnginePkg.Shader import Shader
from GamePkg.Cube import Cube
from GamePkg.SharedShaders import WorldCubeShader_vs, WorldCubeShader_fs
from EnginePkg.WindowSystem import WindowSystem #TODO move this to a better location after initial testing

import glm

class CaveMakerEngine(Engine):
    def __init__(self) -> None:
        super().__init__()
        #temp
        self.cube = None #TODO must wait on opengl resources
        self.debug_camera = None

    def v_create_window(self):
        ret = super().v_create_window()

        #TODO move this, temp code to get things working
        self.cube = Cube()
        self.cube_shader = Shader(vertex_src=WorldCubeShader_vs, fragment_src=WorldCubeShader_fs)
        self.debug_camera = CameraBase()
        self.debug_camera.bind_to_window_input(WindowSystem.get().primary_window.glfw_window)
        self.debug_camera.set_world_position(glm.vec3(0,0,2))

        return ret
    
    def v_render(self, delta_sec: float):
        ''' note: add temporary testing code for initial engine iteration here, but do not check it in. '''
        super().v_render(delta_sec)
        glClearColor(1,0,0,0) 
        glClear(GL_COLOR_BUFFER_BIT)

        self.debug_camera.tick(delta_sec)
        
        if self.cube is not None and self.cube_shader is not None:
            self.cube_shader.use()
            view_mat:glm.mat4 = self.debug_camera.get_view_mat()
            proj_mat:glm.mat4 = self.debug_camera.get_projection_mat()
            self.cube_shader.set_uniform_mat4("view", view_mat)
            self.cube_shader.set_uniform_mat4("projection", proj_mat)
            self.cube.render()

    
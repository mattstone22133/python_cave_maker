import sys, os;myPath = os.path.dirname(os.path.abspath(__file__));sys.path.insert(0, myPath + '/../') #fix relative includes

from OpenGL.GL import *
from EnginePkg.GpuResourceSystem import GpuResource

class Shader(GpuResource):
    def __init__(self, 
    vertex_src:str=None,
    fragment_src:str=None,
    geometry_src:str=None):
        ''' shaders are constructed when opengl resources are available. Prefer sharing shader objects, instead of recreating them 
        as shaders are gpu resources and duplicating them is unnecssary, wasteful, and slow.  .'''
        super().__init__()
        self.vertex_src = vertex_src
        self.fragment_src = fragment_src
        self.geometry_src = geometry_src
        
        self.linked_program = None

    def use(self):
        if self.has_resources:
            glUseProgram(self.linked_program)

    def v_acquire_resources(self):
        super().v_acquire_resources()
        if self.is_gpu_available and self.linked_program is None:
            assert(self.vertex_src is not None and self.fragment_src is not None) #required shaders

            # make the individual shaders
            vertex_shader_id:GLuint  = glCreateShader(GL_VERTEX_SHADER)
            if vertex_shader_id is None:
                print("failed create vertex shader")
            fragment_shader_id:GLuint = glCreateShader(GL_FRAGMENT_SHADER)
            if fragment_shader_id is None:
                print("failed create fragment shader")
            geometry_shader_id:GLuint = None # geometry shaders are optional
            if self.geometry_src is not None:
                geometry_shader_id = glCreateShader(GL_GEOMETRY_SHADER)
                if geometry_shader_id is None:
                    print("failed to create optionally provided geometry shader")

            # update gpu with shader source text
            glShaderSource(vertex_shader_id, self.vertex_src)
            glShaderSource(fragment_shader_id, self.fragment_src)
            if self.geometry_src is not None: glShaderSource(geometry_shader_id, self.geometry_src)

            # compile shaders on gpu
            glCompileShader(vertex_shader_id)
            glCompileShader(fragment_shader_id)
            if geometry_shader_id: glCompileShader(geometry_shader_id)

            vert_result = glGetShaderiv(vertex_shader_id, GL_COMPILE_STATUS)
            if not glGetShaderiv(vertex_shader_id, GL_COMPILE_STATUS):
                print("failed to compile vertex shader:", glGetShaderInfoLog(vertex_shader_id))
                return
            if not glGetShaderiv(fragment_shader_id, GL_COMPILE_STATUS):
                print("failed to compile fragment shader", glGetShaderInfoLog(fragment_shader_id))
                return
            if geometry_shader_id:
                if not glGetShaderiv(geometry_shader_id, GL_COMPILE_STATUS):
                    print("failed to compile geometry shader", glGetShaderInfoLog(geometry_shader_id))
                    return

            # link shaders togeher into a single shader program
            self.linked_program = glCreateProgram() 
            if not self.linked_program:
                print("failed to create shader program")
                return

            glAttachShader(self.linked_program, vertex_shader_id)
            glAttachShader(self.linked_program, fragment_shader_id)
            if geometry_shader_id:
                glAttachShader(self.linked_program, geometry_shader_id)

            glLinkProgram(self.linked_program)
            if not glGetProgramiv(self.linked_program, GL_LINK_STATUS):
                print("failed to link individual shaders into shader program", glGetProgramInfoLog(self.linked_program))
                return 

            # clean up tempoary shader objects now that shader has been linked
            glDeleteShader(vertex_shader_id)
            glDeleteShader(fragment_shader_id)
            if geometry_shader_id: glDeleteShader(geometry_shader_id)
    
    def v_release_resources(self):
        super().v_release_resources()
        if self.linked_program and self.gpu_ready():
            glDeleteProgram(self.linked_program)

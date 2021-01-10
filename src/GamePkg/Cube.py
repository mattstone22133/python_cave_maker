#allow importing form directories above this
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

#class imports
from EnginePkg.GpuResourceSystem import GpuResource
from EnginePkg.Engine import Engine
import glm
from OpenGL.GL import *
from array import array

class Cube(GpuResource):
    static_vert_positions = [
        #x     y       z           
		-0.5, -0.5, -0.5,     	
		0.5, -0.5, -0.5,        
		0.5,  0.5, -0.5,        
		0.5,  0.5, -0.5,        
		-0.5,  0.5, -0.5,       
		-0.5, -0.5, -0.5,       

		-0.5, -0.5,  0.5,       
		0.5, -0.5,  0.5,        
		0.5,  0.5,  0.5,        
		0.5,  0.5,  0.5,        
		-0.5,  0.5,  0.5,       
		-0.5, -0.5,  0.5,       

		-0.5,  0.5,  0.5,       
		-0.5,  0.5, -0.5,       
		-0.5, -0.5, -0.5,       
		-0.5, -0.5, -0.5,       
		-0.5, -0.5,  0.5,       
		-0.5,  0.5,  0.5,       

		0.5,  0.5,  0.5,        
		0.5,  0.5, -0.5,        
		0.5, -0.5, -0.5,        
		0.5, -0.5, -0.5,        
		0.5, -0.5,  0.5,        
		0.5,  0.5,  0.5,        

		-0.5, -0.5, -0.5,       
		0.5, -0.5, -0.5,        
		0.5, -0.5,  0.5,        
		0.5, -0.5,  0.5,        
		-0.5, -0.5,  0.5,       
		-0.5, -0.5, -0.5,       

		-0.5,  0.5, -0.5,       
		0.5,  0.5, -0.5,        
		0.5,  0.5,  0.5,        
		0.5,  0.5,  0.5,        
		-0.5,  0.5,  0.5,     	
		-0.5,  0.5, -0.5      
    ]
    num_verts:int = len(static_vert_positions) // 3

    static_vert_normals = [
    #_____normal_xyz___	  
        0.0,  0.0, -1.0,
        0.0,  0.0, -1.0,	  
        0.0,  0.0, -1.0,	  
        0.0,  0.0, -1.0,	  
        0.0,  0.0, -1.0,  
        0.0,  0.0, -1.0,  
        0.0,  0.0, 1.0,	  
        0.0,  0.0, 1.0,	  
        0.0,  0.0, 1.0,	  
        0.0,  0.0, 1.0,	  
        0.0,  0.0, 1.0,	  
        0.0,  0.0, 1.0,	  
        -1.0,  0.0,  0.0,  
        -1.0,  0.0,  0.0,  
        -1.0,  0.0,  0.0,  
        -1.0,  0.0,  0.0,  
        -1.0,  0.0,  0.0,  
        -1.0,  0.0,  0.0,  
        1.0,  0.0,  0.0,	  
        1.0,  0.0,  0.0,	  
        1.0,  0.0,  0.0,	  
        1.0,  0.0,  0.0,	  
        1.0,  0.0,  0.0,	  
        1.0,  0.0,  0.0,	  
        0.0, -1.0,  0.0,  
        0.0, -1.0,  0.0,	  
        0.0, -1.0,  0.0,	  
        0.0, -1.0,  0.0,	  
        0.0, -1.0,  0.0,  
        0.0, -1.0,  0.0,  
        0.0,  1.0,  0.0,  
        0.0,  1.0,  0.0,	  
        0.0,  1.0,  0.0,	  
        0.0,  1.0,  0.0,	  
        0.0,  1.0,  0.0,
        0.0,  1.0,  0.0  
    ];
    static_vert_uvs = [
        # s     t
        0.0, 0.0,
        1.0, 0.0,
        1.0, 1.0,
        1.0, 1.0,
        0.0, 1.0,
        0.0, 0.0,
        0.0, 0.0,
        1.0, 0.0,
        1.0, 1.0,
        1.0, 1.0,
        0.0, 1.0,
        0.0, 0.0,
        1.0, 0.0,
        1.0, 1.0,
        0.0, 1.0,
        0.0, 1.0,
        0.0, 0.0,
        1.0, 0.0,
        1.0, 0.0,
        1.0, 1.0,
        0.0, 1.0,
        0.0, 1.0,
        0.0, 0.0,
        1.0, 0.0,
        0.0, 1.0,
        1.0, 1.0,
        1.0, 0.0,
        1.0, 0.0,
        0.0, 0.0,
        0.0, 1.0,
        0.0, 1.0,
        1.0, 1.0,
        1.0, 0.0,
        1.0, 0.0,
        0.0, 0.0,
        0.0, 1.0
    ]
    def __init__(self)->None:
        super().__init__()
        self.vao_cube = None
        self.vbo_pos = None
        self.vbo_normal = None
        self.vbo_uv = None

        self.make_vbos()
        #TODO need shutdown event phases, etc.
        pass

    def v_acquire_resources(self):
        '''hook into this virtual to request your gpu resources, such as buffers, shaders, etc)'''
        super().v_acquire_resources()
        self.make_vbos()

    def v_release_resources(self):
        '''hook into this virtual to delete your gpu resources'''
        super().v_release_resources()
        if self.gpu_ready and self.gpu_ready():
            if self.vao_cube:
                glDeleteVertexArrays(self.vao_cube)
            if self.vbo_pos:
                glDeleteBuffers(1, self.vbo_pos)
            if self.vbo_normal:
                glDeleteBuffers(1, self.vbo_normal)
            if self.vbo_uv:
                glDeleteBuffers(1, self.vbo_uv)

    def make_vbos(self)->None:
        self.make_position_vbo()
        self.make_normal_vbo()

    def activate_vao(self)->None:
        #subclasse should override this and provide their own VAO if they modify vbos in any way (ordering, contents, etc.)
        if self.vao_cube is None:
            self.vao_cube = glGenVertexArrays(1)
        glBindVertexArray(self.vao_cube)

    def make_position_vbo(self, pos_layout_loc:int = 0)->None:
        if not self.gpu_ready():
            return #if we lost the opengl context, no need to delete

        if self.vbo_pos is None:
            self.activate_vao()

            self.vbo_pos = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo_pos)

            pos_array:array = array("f", self.static_vert_positions)
            glBufferData(GL_ARRAY_BUFFER, pos_array.tobytes(), GL_STATIC_DRAW)
            
            glVertexAttribPointer(pos_layout_loc, 3, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(pos_layout_loc);

    def make_normal_vbo(self):
        if self.vbo_normal is None:
            #TODO make vbo normal
            pass

    def make_uv_vbo(self):
        if self.vbo_uv is None:
            #TODO make vbo normal
            pass

    def render(self):
        if self.vao_cube:
            glBindVertexArray(self.vao_cube)
            glDrawArrays(GL_TRIANGLES, 0, Cube.num_verts) #this division can return float if either arg is float
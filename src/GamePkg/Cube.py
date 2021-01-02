#allow importing form directories above this
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

#class imports
from EnginePkg.Engine import Engine
import glm
from OpenGL.GL import *
from array import array

class Cube:
    static_cube_vao = None
    static_pos_vbo = None
    static_normal_vbo = None
    static_uv_vbo = None
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
        print("made a cube")
        self.make_vbos()
        #TODO need shutdown event phases, etc.
        pass

    def make_vbos(self)->None:
        self.make_position_vbo()
        self.make_normal_vbo()

    def activate_vao(self)->None:
        #subclasse should override this and provide their own VAO if they modify vbos in any way (ordering, contents, etc.)
        if self.static_cube_vao is None:
            self.static_cube_vao = glGenVertexArrays(1)
        glBindVertexArray(self.static_cube_vao)

    def make_position_vbo(self)->None:
        if self.static_pos_vbo is None:
            self.activate_vao()

            self.static_pos_vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.static_pos_vbo)

            pos_array:array = array("f", self.static_vert_positions)
            # glBufferData(GL_ARRAY_BUFFER, pos_array.tostring(), GL_STATIC_DRAW) #tostring was removed in latest version of python
            glBufferData(GL_ARRAY_BUFFER, pos_array.tobytes(), GL_STATIC_DRAW)
            
            pos_layout_loc:int = 0
            glVertexAttribPointer(pos_layout_loc, 3, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(pos_layout_loc);
            
    def make_normal_vbo(self):
        if self.static_normal_vbo is None:
            pass

    def render(self):
        pass
WorldCubeShader_vs = """
#version 330 core
layout (location = 0) in vec3 vert_position;
layout (location = 0) in vec3 vert_normal;
//layout (location = 2) in vec2 vert_uv;

//out vec3 pos;
//out vec3 normal
//out vec2 uv;

uniform mat4 model      = mat4(1.f);
uniform mat4 view       = mat4(1.f);
uniform mat4 projection = mat4(1.f);

void main(){
    //uv = vert_uv;
    //normal = normalize(vert_normal); //normalizing for model loading, this we we know normal is noramlized before interpolation
    gl_Position = projection * view * model * vec4(vert_position, 1);
}
"""

WorldCubeShader_fs = """
#version 330 core
out vec4 fragmentColor;

//in vec3 pos;
//in vec3 normal;
//in vec2 uv;

//uniform sampler2D textureData;

void main(){
    //fragmentColor = texture(textureData, uv);
    fragmentColor = vec4(0.f, 0.f, 1.f, 1.f); 
}
"""
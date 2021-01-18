import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import glm
from src.EnginePkg.SceneNode import Transform, SceneNode

def test_transform():
    #test that run time of basic functions is okay
    a_rotation_transform = Transform()
    a_rotation_transform.position = glm.vec3(0,0,0)
    a_rotation_transform.rotation_quat = glm.angleAxis(glm.radians(180), glm.vec3(0,1,0))
    a_rotation_transform.scale = glm.vec3(1)
    a_model_matrix = a_rotation_transform.get_model_matrix()
    a_rotation_transform.position = glm.vec3(a_model_matrix * glm.vec4(a_rotation_transform.position, 1.0))

    #test rotating a vector around y axis using transforms
    x_transform = Transform(position=glm.vec3(1,0,0))
    x_transform.position = glm.vec3(a_rotation_transform.get_model_matrix() * glm.vec4(x_transform.position, 1.0))
    scalar_projection:float = glm.dot(glm.vec3(-1, 0, 0), x_transform.position)
    assert(scalar_projection > 0.0) #after rotation, position shuld be pointing in -x since this is 180 around y

def test_local_transform_functions():
    a_vec = glm.vec3(1, 2, 3)
    a_rot_quat = glm.angleAxis(glm.radians(34.5), glm.vec3(0,1,0))
    node = SceneNode()

    node.set_local_position(a_vec)
    assert(a_vec == node.get_local_position())

    node.set_local_scale(a_vec)
    assert(a_vec == node.get_local_scale())

    node.set_local_rotation(a_rot_quat)
    assert(a_rot_quat == node.get_local_rotation())

def test_scene_node_children():
    parent = SceneNode()
    child = SceneNode()
    parent.add_child(child)
    assert(len(parent.children) == 1)

    parent.remove_child(child)
    assert(len(parent.children) == 0)

def test_scene_node_world_functions():
    parent_pos = glm.vec3(1,1,1)
    child_pos = glm.vec3(1,1,1)
    parent_scale = 10
    child_scale = 5

    parent = SceneNode()
    parent.set_local_position(parent_pos)
    parent.set_local_rotation(glm.angleAxis(glm.radians(180), glm.normalize(glm.vec3(0,1,0))))

    child = SceneNode()
    parent.add_child(child)
    child.set_local_position(child_pos)
    #this child has no rotation, adding rotation will make positin tests hard to reason about, that will be done in another test
    
    #test child world pos
    child_world_pos = child.get_world_position()
    simulated_position = child_pos + parent_pos
    simulated_position.x = 0 #child should have rotated 180, putting it back at 0 x location, but leaving y alone
    simulated_position.z = 0 #child should have rotated 180, putting it back at 0 z location, but leaving y alone
    assert( glm.length(simulated_position - child_world_pos) < 0.01) # make sure positions are roughly the same

    #test child world rotation
    parent.make_dirty() #dirty parent so we can debug all the matrix caching
    a_vec_to_rotate = glm.vec3(1,1,1)
    # a_vec_to_rotate = glm.vec3(1,0,0)
    child_world_rot = child.get_world_rotation()
    parent_world_rot = parent.get_local_rotation() #parents local is the world rotation
    child_rotated_vec = child_world_rot * a_vec_to_rotate 
    parent_rotated_vec = parent_world_rot * a_vec_to_rotate
    assert( glm.length(child_rotated_vec - parent_rotated_vec) < 0.01)

def test_advanced_world_position():
    #todo robust test set world position
    #todo robust test get world position
    assert(False)#TODO complicated world positioning

def test_advanced_world_rotation():
    #todo robust test set world rotation
    #todo robust test get world rotation
    assert(False)#TODO complicated world rotation


    





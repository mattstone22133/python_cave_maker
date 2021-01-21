import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import glm
from src.EnginePkg.SceneNode import Transform, SceneNode

def vec3_are_same(a_vec:glm.vec3, b_vec:glm.vec3):
    return glm.length(a_vec - b_vec) < 0.001

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
    #test robust get world position
    parent = SceneNode()
    parent_pos = glm.vec3(1,0,0)
    parent.set_local_position(parent_pos)

    child = SceneNode()
    child_pos = glm.vec3(1,0,0)
    child.set_local_position(child_pos)

    parent.add_child(child)

    child_world_pos = child.get_world_position()
    assert(glm.length(child_world_pos - (parent_pos + child_pos)) < 0.01)

    parent.set_local_rotation(glm.angleAxis(glm.radians(180), glm.normalize(glm.vec3(0,1,0))))

    child_world_pos = child.get_world_position()
    assert(glm.length(child_world_pos - ((parent_pos + -child_pos))) < 0.01) #parent still offset to (1,0,0), but rotated so child is now 1 to left of parent, ie at zero

    #robust test set world position
    move_child_to_world_point = glm.vec3(3,3,3)
    child.set_world_position(move_child_to_world_point)
    child_world_pos = child.get_world_position()
    assert(glm.length(child_world_pos - move_child_to_world_point) < 0.01)

    move_child_to_world_point = glm.vec3(-3,-4, 2)
    child.set_world_position(move_child_to_world_point)
    child_world_pos = child.get_world_position()
    assert(glm.length(child_world_pos - move_child_to_world_point) < 0.01)

    move_parent_to_world_point = glm.vec3(1,2,-3)
    parent.set_world_position(move_parent_to_world_point)
    parent_world_pos = parent.get_world_position()
    assert(glm.length(parent_world_pos - move_parent_to_world_point) < 0.01)


def test_advanced_world_rotation():
    parent = SceneNode()
    parent_pos = glm.vec3(1,0,0)
    parent.set_local_position(parent_pos)

    child = SceneNode()
    child_pos = glm.vec3(1,0,0)
    child.set_local_position(child_pos)

    parent.add_child(child)

    def quats_are_equal(a:glm.quat, b:glm.quat):
        #seems that two quaternions can give same rotations, but have different signs
        #so test is making sure they produce the same vector after rotations; this could probably be more robust
        a_vec = glm.vec3(1,1,1)* a
        b_vec = glm.vec3(1,1,1)* b
        return glm.length(a_vec - b_vec) < 0.01

    # robust test get world rotation
    start_rot = glm.angleAxis(glm.radians(180), glm.normalize(glm.vec3(0,1,0)))
    parent.set_local_rotation(start_rot)
    child_world_rot = child.get_world_rotation()
    assert(quats_are_equal(child_world_rot, start_rot))
    assert(not quats_are_equal(child.get_local_rotation(), start_rot))

    #todo robust test set world rotation
    arbitrary_rot = glm.angleAxis(glm.radians(180), glm.normalize(glm.vec3(1,-1,1)))
    child.set_world_rotation(arbitrary_rot)
    child_world_rot = child.get_world_rotation()
    assert(quats_are_equal(child_world_rot, arbitrary_rot))
    assert(not quats_are_equal(child.get_local_rotation(), arbitrary_rot))
    assert(not quats_are_equal(parent.get_world_rotation(), arbitrary_rot))

    arbitrary_rot = glm.angleAxis(glm.radians(-33.6), glm.normalize(glm.vec3(1,-1,1)))
    child.set_world_rotation(arbitrary_rot)
    child_world_rot = child.get_world_rotation()
    assert(quats_are_equal(child_world_rot, arbitrary_rot))
    assert(not quats_are_equal(child.get_local_rotation(), arbitrary_rot))
    assert(not quats_are_equal(parent.get_world_rotation(), arbitrary_rot))

def test_world_foward_right_up_vecs():
    parent = SceneNode()
    parent_pos = glm.vec3(1,0,0)
    parent.set_local_position(parent_pos)

    child = SceneNode()
    child_pos = glm.vec3(1,0,0)
    child.set_local_position(child_pos)

    parent.add_child(child)
    start_rot = glm.angleAxis(glm.radians(180), glm.normalize(glm.vec3(0,1,0)))
    parent.set_local_rotation(start_rot)

    #did not change local transform, make sure these match up
    assert(vec3_are_same(child._forward, child.get_local_forward()))
    assert(vec3_are_same(child._right, child.get_local_right()))
    assert(vec3_are_same(child._up, child.get_local_up()))

    #180 around y should make vectorspoint in opposite directions
    assert(vec3_are_same(-child._forward, child.get_world_forward()))
    assert(vec3_are_same(-child._right, child.get_world_right()))
    assert(vec3_are_same(child._up, child.get_world_up()))

    #parent should match child world as we have only rotated the parent
    assert(vec3_are_same(parent.get_world_forward(), child.get_world_forward()))
    assert(vec3_are_same(parent.get_world_right(), child.get_world_right()))
    assert(vec3_are_same(parent.get_world_up(), child.get_world_up()))

    counter_rot = glm.angleAxis(glm.radians(-180), glm.normalize(glm.vec3(0,1,0)))
    child.set_local_rotation(counter_rot)

    #we counteracted the parent rotation, make sure the child now matches its original vectors
    assert(vec3_are_same(child._forward, child.get_world_forward()))
    assert(vec3_are_same(child._right, child.get_world_right()))
    assert(vec3_are_same(child._up, child.get_world_up()))

    #we now have a local rotation, the child local forward/right/up should not match its default axis (because local doesn't consider parent)
    assert(not vec3_are_same(child._forward, child.get_local_forward()))
    assert(not vec3_are_same(child._right, child.get_local_right()))
    assert(vec3_are_same(child._up, child.get_local_up())) #we never changed the up vector

    





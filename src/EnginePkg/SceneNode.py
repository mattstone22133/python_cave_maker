import glm
import weakref
from typing import List

identity = glm.mat4()

##########################################################################################################
# Transform Wrapper
#   consider using a SceneNode rather than this directly.
##########################################################################################################
class Transform:
    def __init__(self, position = glm.vec3(0.0, 0.0, 0.0), rotation = glm.quat(), scale = glm.vec3(1.0, 1.0, 1.0)) -> None:
        self.position:      glm.vec3 = glm.vec3(position)
        self.rotation_quat: glm.quat = glm.quat(rotation)
        self.scale:         glm.vec3 = glm.vec3(scale)

    def get_model_matrix(self)->glm.mat4:
        model = glm.mat4() #newer glm versions do not need 1.0f to create identity matrix
        model = glm.translate(model, self.position)
        model = model * glm.mat4_cast(self.rotation_quat)
        model = glm.scale(model, self.scale)
        return model

##########################################################################################################
# Scene Nodes
##########################################################################################################
local_forward = glm.vec3(0,0,-1)
local_right = glm.vec3(1,0,0)
local_up = glm.vec3(0,1,0)
class SceneNode:
    def __init__(self, local_transform=Transform(), strong_parent:'SceneNode'=None) -> None:
        self._local_transform:Transform = Transform(local_transform.position, local_transform.rotation_quat, local_transform.scale) 
        self.weak_parent = weakref.ref(strong_parent) if strong_parent is not None else None
        self.children:List[SceneNode] = []
        # scene nodes are lazy, if a needed matrix is null then the node is dirty and requires a clean
        self.make_dirty() #define cache variables in single location, make_dirty will init them

    def make_dirty(self):
        self._world_mat4_cache:glm.mat4 = None
        self._parent_world_mat4_cache:glm.mat4 = None
        self._world_pos_cache:glm.vec3 = None
        self._world_rot_cache:glm.quat = None
        self._world_scale_cache:glm.vec3 = None
        for child in self.children:
            child.make_dirty() # required if children are not subscribing to parents (to avoid circular ref)

    def add_child(self, child_node:'SceneNode'):
        if child_node not in self.children:
            old_parent = child_node.weak_parent() if child_node.weak_parent is not None else None
            if old_parent:
                old_parent.remove_child(child_node)
            child_node.weak_parent = weakref.ref(self)
            self.children.append(child_node)
            self.make_dirty()

    def remove_child(self, child_node:'SceneNode'):
        if child_node in self.children:
            child_node.weak_parent = None
            self.children.remove(child_node)

    # Local Transform Functions
    def set_local_position(self, position:glm.vec3):
        self._local_transform.position = glm.vec3(position)
        self.make_dirty()
    def get_local_position(self):
        return glm.vec3(self._local_transform.position)
    def set_local_rotation(self, rotation:glm.quat):
        self._local_transform.rotation_quat = glm.quat(rotation)
        self.make_dirty()
    def get_local_rotation(self):
        return glm.quat(self._local_transform.rotation_quat)
    def set_local_scale(self, scale:glm.vec3):
        self._local_transform.scale = glm.vec3(scale)
        self.make_dirty()
    def get_local_scale(self):
        return glm.vec3(self._local_transform.scale)

    # World Transform Functions
    def get_parent_world_matrix(self)->glm.mat4:
        if self._parent_world_mat4_cache is None:
            parent = self.weak_parent() if self.weak_parent is not None else None
            if parent is not None:
                self._parent_world_mat4_cache = parent.get_world_transform_matrix()
            else:
                self._parent_world_mat4_cache = glm.mat4() #identity
        return self._parent_world_mat4_cache

    def get_world_transform_matrix(self)->glm.mat4:
        if self._world_mat4_cache is None:
            parent_matrix = self.get_parent_world_matrix()
            self._world_mat4_cache = parent_matrix * self._local_transform.get_model_matrix()
        return self._world_mat4_cache

    def get_world_position(self) -> glm.vec3:
        if self._world_pos_cache is None:
            self._world_pos_cache = glm.vec3( self.get_world_transform_matrix() * glm.vec4(0,0,0,1) )
        return self._world_pos_cache

    # not supporting get/set world scale at this time due to complications in implementation with signed rotaitons
    # def get_world_scale(self) -> glm.vec3:
    #     if self._world_scale_cache is None:
    #         #get world scale is hard, you cannot simply multply all scales together, rotations matter (thought excerise: I think this can be shown, in blender, with 3 parent nodes, you can scale down grandparent's x, and influence child's y scale, if middle-parent is rotated by 90)
    #         #note: it apperas that getting scale from final world transform may include incorrect negatives based on values close to zero that are negative; only considering scale concatenations, 
    #         # though this many not be strictly correct considering rotations
    #         #### self._world_scale_cache = glm.vec3( self.get_world_transform_matrix() * glm.vec4(1,1,1,0) )
    #         parent_scale = self.weak_parent().get_world_scale() if self.weak_parent is not None else glm.vec3(1,1,1)
    #         self._world_scale_cache = parent_scale * self._local_transform.scale
    #     return self._world_scale_cache

    def get_world_rotation(self) -> glm.quat:
        if self._world_rot_cache is None:
            # NOTE: the commented code below appears to work, but probably more effecient to extra quaterions directly; leaving
            basis_mat = glm.mat3() #identiy matrix where each column is a basis vector; x, y, and z
            transformed_basis_mat = glm.mat3(self.get_world_transform_matrix()) * basis_mat 
            self._world_rot_cache = glm.quat_cast(transformed_basis_mat)
            #alternative: just consider parent world rotations
            # parent_rot = self.weak_parent().get_world_rotation() if self.weak_parent is not None else glm.quat()
            # self._world_rot_cache = parent_rot * self._local_transform.rotation_quat
        return self._world_rot_cache
    
        



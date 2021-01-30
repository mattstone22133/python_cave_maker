
from EnginePkg.Engine import Engine
from EnginePkg.SceneNode import SceneNode
import glfw
import glm

class CameraBase(SceneNode):
    def __init__(self) -> None:
        super().__init__()
        self.input_bound_window = None
        self.fov_rad = glm.radians(45)
        self.near = 0.1
        self.far = 1000
        self.fly_speed = 1.0 #meters_per_sec
        self.mouse_sensitivity = 0.01
        self._set_up_transient_cache_variables()

    def _set_up_transient_cache_variables(self):
        self.last_mouse_x = 0
        self.last_mouse_y = 0

    def get_view_mat(self) -> glm.mat4:
        world_pos = self.get_world_position()
        world_forward = self.get_world_forward()
        world_up = self.get_world_up()
        return glm.lookAt(world_pos, world_pos + world_forward, world_up) 

    def get_projection_mat(self) -> glm.mat4:
        from .WindowSystem import Window, WindowSystem
        aspect = 1
        win_sys = WindowSystem.get()
        if win_sys.primary_window is not None:
            aspect = win_sys.primary_window.get_aspect()
        return glm.perspective(self.fov_rad, aspect, self.near, self.far )
        
    def bind_to_window_input(self, glfw_window)->None:
        # todo proper input subscription system
        # todo create unbind input function 
        if self.input_bound_window is not None:
            glfw.set_cursor_pos_callback(self.input_bound_window, None)
            glfw.set_key_callback(self.input_bound_window, None)
        if glfw_window is not None:
            glfw.set_cursor_pos_callback(glfw_window, self.handle_cursor_moved)
            glfw.set_key_callback(glfw_window, self.handle_key)
        self.input_bound_window = glfw_window #set/clear

    def set_mouse_capture(self, glfw_window, capture_mouse:bool)->None:
        if glfw_window is not None:
            glfw.set_input_mode(glfw_window, glfw.CURSOR, glfw.CURSOR_DISABLED if capture_mouse else glfw.CURSOR_NORMAL )
            pass

    def handle_cursor_moved(self, glfw_window, xpos:float, ypos:float):
        # print("mouse pos", xpos, ypos)
        delta_x = xpos - self.last_mouse_x
        delta_y = ypos - self.last_mouse_y
        self.last_mouse_x = xpos
        self.last_mouse_y = ypos

        u_axis:glm.vec3 = self.get_local_right() 
        v_axis:glm.vec3 = self.get_local_up()
        w_axis:glm.vec3 = self.get_local_forward()
        pitch_factor = delta_y
        yaw_factor = delta_x

        uv_plane_vec:glm.vec3 = u_axis * yaw_factor +  v_axis * -pitch_factor
        rotation_magnitude:float = glm.length(uv_plane_vec);
        if rotation_magnitude == 0.0:
            return
        uv_plane_vec = glm.normalize(uv_plane_vec)
        rotation_axis:glm.vec3 = glm.normalize(glm.cross(uv_plane_vec, -w_axis)) #get a rotation axis between the vector in the screen and the direction of the camera.
		# rotate the w_axis
        rot_quat:glm.quat = glm.angleAxis(self.mouse_sensitivity * rotation_magnitude, rotation_axis)

        old_quat = self.get_local_rotation()
        new_quat = rot_quat * old_quat
        self.set_local_rotation(new_quat)

    def handle_key(self, glfw_window, key:int, scanecode:int, action:int, mods:int)->None:
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS: #actions: glfw.PRESS, glfw.RELEASE, glfw.REPEAT
            in_cursor_mode = (glfw.get_input_mode(glfw_window, glfw.CURSOR) == glfw.CURSOR_NORMAL)
            self.set_mouse_capture(glfw_window, in_cursor_mode)


    def tick(self, dt_sec:float)->None:
        #todo with proper input system, just monitor state of keys rather than polling window each frame?
        if self.input_bound_window is not None:
            self.input_vector = glm.vec3(0,0,0)
            if glfw.get_key(self.input_bound_window, glfw.KEY_W) == glfw.PRESS:
                self.input_vector.x += 1
            if glfw.get_key(self.input_bound_window, glfw.KEY_S) == glfw.PRESS:
                self.input_vector.x += -1
            if glfw.get_key(self.input_bound_window, glfw.KEY_A) == glfw.PRESS:
                self.input_vector.z += -1
            if glfw.get_key(self.input_bound_window, glfw.KEY_D) == glfw.PRESS:
                self.input_vector.z += 1
            if glm.length2(self.input_vector) > 0.001:
                local_pos = self.get_local_position()
                local_pos = local_pos + self.get_local_forward() * self.input_vector.x * dt_sec
                local_pos = local_pos + self.get_local_right() * self.input_vector.z * dt_sec
                self.set_local_position(local_pos)
            

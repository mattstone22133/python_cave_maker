
from EnginePkg.Engine import Engine
from EnginePkg.SceneNode import SceneNode
import glfw
import glm

class CameraBase(SceneNode):
    def __init__(self) -> None:
        super().__init__()
        self.input_bound_window = None
        
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
        print("mouse pos", xpos, ypos)

    def handle_key(self, glfw_window, key:int, scanecode:int, action:int, mods:int)->None:
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS: #actions: glfw.PRESS, glfw.RELEASE, glfw.REPEAT
            in_cursor_mode = (glfw.get_input_mode(glfw_window, glfw.CURSOR) == glfw.CURSOR_NORMAL)
            self.set_mouse_capture(glfw_window, in_cursor_mode)
        print("key pressed ", key, scanecode, action, mods)

    def tick(self, dt_sec:float)->None:
        #todo with proper input system, just monitor state of keys rather than polling window each frame?
        if self.input_bound_wndow is not None:
            if glfw.get_key(self.input_bound_wndow, glfw.KEY_W) == glfw.PRESS:
                print("w")
            if glfw.get_key(self.input_bound_wndow, glfw.KEY_S) == glfw.PRESS:
                print("s")
            if glfw.get_key(self.input_bound_wndow, glfw.KEY_A) == glfw.PRESS:
                print("a")
            if glfw.get_key(self.input_bound_wndow, glfw.KEY_D) == glfw.PRESS:
                print("d")

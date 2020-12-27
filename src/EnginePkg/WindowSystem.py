# from Engine import get_engine
from .SystemBase import SystemBase

import OpenGL.GL as gl
import sys
import glfw

#########################################################################################
# Window Wrapper
#########################################################################################
class Window:
    def __init__(self) -> None:
        super().__init__()

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, 1)

        self.glfw_window = glfw.create_window(int(1920/2), int(1040/2), "OpenGl", None, None)
        if self.glfw_window is None:
            print("failed to create a window")
            glfw.terminate()
            sys.exit()

        glfw.make_context_current(self.glfw_window)

    def update_screen(self):
        if self.glfw_window is not None:
            glfw.swap_buffers(self.glfw_window)
            glfw.poll_events()


#########################################################################################
# Window System
#########################################################################################
class WindowSystem(SystemBase):
    def __init__(self) -> None:
        super().__init__()
        self.primary_window:Window = None

    # -- api --
    def create_default_window(self):
        self.primary_window = Window()

    def primary_window_active(self)->bool:
        if self.primary_window is None:
            return False
        
        return glfw.window_should_close(self.primary_window.glfw_window)

    # -- virtuals --
    def init_system_v(self):
        if not glfw.init(): 
            print("failed to init glfw")
            sys.exit()        

        #todo remove me, testing circular dependency
        from .Engine import get_engine, Engine
        isntance:Engine = get_engine()

        return super().init_system_v()

    def shutdown_system_v(self):
        glfw.terminate() #may need to special case this if other systems depend on window/opengl context
        return super().shutdown_system_v()

    

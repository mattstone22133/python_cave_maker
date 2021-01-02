# from Engine import get_engine
from .SystemBase import SystemBase
from .EventObject import Event

import OpenGL.GL as gl
import sys
import glfw

#########################################################################################
# Event Args
#########################################################################################
class EventArgs_GpuResourceChanged:
    def __init__(self, has_resources:bool):
        self.has_resources:bool = has_resources

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
        self.event_gpu_resources_changed = Event(EventArgs_GpuResourceChanged)

    #### api ####
    def create_default_window(self):
        self.primary_window = Window()
        self.event_gpu_resources_changed.broadcast(EventArgs_GpuResourceChanged(has_resources=True));

    def primary_window_active(self)->bool:
        if self.primary_window is None:
            return False
        
        return glfw.window_should_close(self.primary_window.glfw_window)

    #### virtuals ####
    def init_system_v(self):
        if not glfw.init(): 
            print("failed to init glfw")
            sys.exit()        

        #todo remove me, testing circular dependency
        from .Engine import get_engine, Engine
        isntance:Engine = get_engine()

        return super().init_system_v()

    def shutdown_system_v(self):
        if self.primary_window is not None:
            self.event_gpu_resources_changed.broadcast(EventArgs_GpuResourceChanged(has_resources=False)) #signal release before terminating
        glfw.terminate() #may need to special case this if other systems depend on window/opengl context
        return super().shutdown_system_v()

def get_window_system() -> WindowSystem:
    '''convenience static function for getting window system'''
    from .Engine import get_engine, Engine
    engine:Engine = get_engine()
    return engine.window_system
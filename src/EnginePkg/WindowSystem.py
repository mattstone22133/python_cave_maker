# from Engine import get_engine
from OpenGL.GL import *
from .SystemBase import SystemBase
from .EventObject import Event

import OpenGL.GL as gl
import sys
import glfw

#########################################################################################
# OpenGL Error Checking
#########################################################################################
def opengl_debug_message_callback(source:GLenum, msg_type:GLenum, id:GLuint, severity:GLenum, length:GLsizei, raw, user):
    converted_message = raw[0:length]
    print('opengl error: ', source, msg_type, id, severity, converted_message)

#########################################################################################
# Event Args
#########################################################################################
class EventArgs_GpuResourceChanged:
    def __init__(self, gpu_ready:bool):
        self.gpu_ready:bool = gpu_ready

#########################################################################################
# Window Wrapper
#########################################################################################
class Window:
    def __init__(self) -> None:
        super().__init__()
        debug_opengl = False

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3 if not debug_opengl else 4) #4 to get opengl debug callback
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, 1)
        glfw.window_hint(glfw.OPENGL_DEBUG_CONTEXT, debug_opengl)

        self.glfw_window = glfw.create_window(int(1920/2), int(1040/2), "OpenGl", None, None)
        if self.glfw_window is None:
            print("failed to create a window")
            glfw.terminate()
            sys.exit()

        glfw.make_context_current(self.glfw_window)
        if debug_opengl:
            glDebugMessageCallback(GLDEBUGPROC(opengl_debug_message_callback), None)


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
        self.register_primary_window(Window())
        self.event_gpu_resources_changed.broadcast(EventArgs_GpuResourceChanged(gpu_ready=True))

    def primary_window_active(self)->bool:
        if self.primary_window is None:
            return False
        return glfw.window_should_close(self.primary_window.glfw_window)

    #### virtuals ####
    def v_init_system(self):
        if not glfw.init(): 
            print("failed to init glfw")
            sys.exit()        
        return super().v_init_system()

    def v_tick_system(self, dt_sec:float):
        if self.primary_window:
            assert(self.primary_window.registered_as_primary_window) #someone installed a primary window without registering it, we need to register for callbacks.

    def v_shutdown_system(self):
        if self.primary_window is not None:
            self.event_gpu_resources_changed.broadcast(EventArgs_GpuResourceChanged(gpu_ready=False)) #signal release before terminating
        glfw.terminate() #may need to special case this if other systems depend on window/opengl context
        return super().v_shutdown_system()

    def register_primary_window(self, window:Window):
        # cleanup previous window 
        if self.primary_window:
            glfw.set_window_close_callback(self.primary_window.glfw_window, None)
            self.primary_window.registered_as_primary_window = False
        if window:
            glfw.set_window_close_callback(window.glfw_window, self.primary_window_closing)
        self.primary_window = window
        self.primary_window.registered_as_primary_window = True

    def primary_window_closing(self, window):
        print("window close event detected")
        self.event_gpu_resources_changed.broadcast(EventArgs_GpuResourceChanged(gpu_ready=False))

def get_window_system() -> WindowSystem:
    '''convenience static function for getting window system'''
    from .Engine import get_engine, Engine
    engine:Engine = get_engine()
    return engine.window_system
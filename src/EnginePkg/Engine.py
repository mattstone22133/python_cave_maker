
import OpenGL.GL as gl
from typing import List

from .EventObject import Event
from .SystemBase import SystemBase
from .TimeSystem import TimeSystem, TimeManager
from .WindowSystem import WindowSystem
from .GpuResourceSystem import GpuResourceSystem

'''
A module static singleton.
This allows for modular code testing by just cleaning up.
Subclassing engine will correctly register singleton if super is called in __init__
'''
singleton = None

class Engine:

    def __init__(self) -> None:
        super().__init__()
        global singleton
        if singleton is not None:
            print("warning: starting engine singleton but one already exists and will be cleared")
        singleton = self
        #systems
        self.systems:List[SystemBase] = []
        self.time_system:TimeSystem = TimeSystem() #time system requires special handling as it influences managing ticking systems
        self.window_system = self.register_system(WindowSystem())
        self.gpu_resource_system = self.register_system(GpuResourceSystem())
        #events
        self.event_render:Event = Event()

    def run(self):
        self.initialize_systems()
        self.game_loop()
        self.shutdown_systems()

    def initialize_systems(self):
        print("initializing systems")
        for system in self.systems:
            system.v_init_system()

    def game_loop(self):
        print("starting game loop")

        self.v_create_window()

        while not self.window_system.primary_window_active():
            self.time_system.update_time()
            for system in self.systems:
                system.v_tick_system(self.time_system.frame_delta_sec)
            self.v_render(self.time_system.frame_delta_sec) #todo get delta time and pass it
            self.event_render.broadcast({"delta_sec" : self.time_system.frame_delta_sec})
            self.window_system.primary_window.update_screen()

    def shutdown_systems(self):
        print("shutting down systems")
        for system in self.systems:
            system.v_shutdown_system()

    def register_system(self, system:SystemBase)->SystemBase:
        if system not in self.systems:
            self.systems.append(system)
            return system
        else:
            print("failed tor egister duplicate system")
            return None

    # overrides
    def v_create_window(self):
        self.window_system.create_default_window()

    def v_render(self, delta_sec:float):
        pass


def get_engine()->Engine:
    return singleton



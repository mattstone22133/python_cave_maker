
import OpenGL.GL as gl
from typing import List

from .EventObject import Event
from .SystemBase import SystemBase
from .TimeSystem import TimeSystem, TimeManager
from .WindowSystem import WindowSystem

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
        #events
        self.event_render:Event = Event()

    def run(self):
        self.initialize_systems()
        self.game_loop()
        self.shutdown_systems()

    def initialize_systems(self):
        print("initializing systems")
        for system in self.systems:
            system.init_system_v()

    def game_loop(self):
        print("starting game loop")

        self.create_window_v()

        while not self.window_system.primary_window_active():
            self.time_system.update_time()
            self.render_v(self.time_system.frame_delta_sec) #todo get delta time and pass it
            self.event_render.broadcast({"delta_sec" : self.time_system.frame_delta_sec})
            self.window_system.primary_window.update_screen()

    def shutdown_systems(self):
        print("shutting down systems")
        for system in self.systems:
            system.shutdown_system_v()

    def register_system(self, system:SystemBase)->SystemBase:
        if system not in self.systems:
            self.systems.append(system)
            return system
        else:
            print("failed tor egister duplicate system")
            return None

    # overrides
    def create_window_v(self):
        self.window_system.create_default_window()

    def render_v(self, delta_sec:float):
        pass


def get_engine()->Engine:
    return singleton



from typing import List
from .SystemBase import SystemBase
import glfw
import glm

MAX_DELTA_TIME_SEC:float = 0.5

class TimeManager:
    def __init__(self) -> None:
        super().__init__()
        self.time_dilation_factor:float = 1.0
        self.dilated_delta_sec:float = 0.0
        self.total_time_passed:float = 0.0

    def update(self, raw_delta_sec:float):
        this_frame_dilation = self.time_dilation_factor #don't allow dilation changes mid update; next frame will take changes
        self.dilated_delta_sec = this_frame_dilation * raw_delta_sec
        self.total_time_passed += self.dilated_delta_sec
        #todo tick timers
        #todo add/remove defferred timers
        #todo tickgroups


class TimeSystem(SystemBase):
    def __init__(self) -> None:
        super().__init__()
        self.time_managers:List[TimeManager] = []
        self.last_frame_time:float = 0.0
        self.frame_delta_sec:float = 0.0
        self.currently_updating_time:bool = False

    def update_time(self)-> None:
        current_timestamp:float = glfw.get_time()
        self.frame_delta_sec: float = current_timestamp - self.last_frame_time
        self.frame_delta_sec = glm.clamp(self.frame_delta_sec, 0.0, MAX_DELTA_TIME_SEC)
        self.last_frame_time = current_timestamp

        self.currently_updating_time = True
        for time_manager in self.time_managers:
            time_manager.update(self.frame_delta_sec)
        self.currently_updating_time = False
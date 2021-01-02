from .SystemBase import SystemBase
from typing import List

class GpuResource:
    def __init__(self):
        super().__init__()
        self.has_resources: bool = False

        from .Engine import Engine, get_engine
        get_engine().gpu_resource_system.add(self)

    def acquire_resources_v(self):
        '''hook into this virtual to request your gpu resources, such as buffers, shaders, etc)'''
        self.has_resources = True

    def release_resources_v(self):
        '''hook into this virtual to delete your gpu resources'''
        self.has_resources = False


class GpuResourceSystem(SystemBase):
    '''GPU resource management. If something requires GPU resources (eg shaders, buffers, textures), then it requires management and clenaup.
    This system tacks all GpuResource objects and is responsible for telling said objects to acquire their resources or release them'''

    def __init__(self):
        super().__init__()
        self.active_resources: List[GpuResource] = []
        self.pending_add: List[GpuResource] = []
        self.resources_available = False #TODO hook this up to window system

    def init_system_v(self):
        # window system is now gauranteed to be instantiated
        from .WindowSystem import WindowSystem, get_window_system
        win_sys:WindowSystem = get_window_system()
        win_sys.event_gpu_resources_changed.add_subscriber(self.handle_gpu_resources_changed)

    def handle_gpu_resources_changed(self, args)->None:
        from .WindowSystem import EventArgs_GpuResourceChanged
        typed_args:EventArgs_GpuResourceChanged = args #avoiding adding type to parameter as dont want to create circular dependency on systems

        if typed_args.has_resources:
            self.resources_available = True
        else:
            self.resources_available = False

    def shutdown_system_v(self):
        self.release_resources()

    def tick_system_v(self, dt_sec:float):
        if self.resources_available:
            for new_resource in self.pending_add:
                new_resource.acquire_resources_v()
        else:
            self.release_resources()

    def release_resources(self):
        for active_resource in self.active_resources:
            active_resource.release_resources_v

    def add(self, resource: GpuResource):
        if (resource is not None
        and resource not in self.active_resources 
        and resource not in self.pending_add):
            self.pending_add.add(resource)


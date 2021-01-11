from .SystemBase import SystemBase
from typing import List

class GpuResource:
    def __init__(self):
        super().__init__()
        self.has_resources: bool = False
        self.is_gpu_available: bool = False

        from .Engine import Engine, get_engine
        get_engine().gpu_resource_system._add(self)

    def _acquire_resources(self):
        '''Only GpuResourceSystem should call this method, so that state is always in correct configuration'''
        self.v_acquire_resources()
        assert(self.has_resources) # catch if child forgot to call super

    def _release_resources(self):
        '''Only GpuResourceSystem should call this method, so that state is always in correct configuration'''
        self.v_release_resources()
        assert(not self.has_resources) # catch if child forgot to call super

    def v_acquire_resources(self):
        '''hook into this virtual to request your gpu resources, such as buffers, shaders, etc)
            This should never invoked by a subclass, let the GPU resource system do so state is maintained '''
        self.has_resources = True

    def v_release_resources(self):
        '''hook into this virtual to delete your gpu resources
            This should never invoked by a subclass, let the GPU resource system do so state is maintained '''
        self.has_resources = False

    def gpu_ready(self)->bool:
        return self.is_gpu_available


class GpuResourceSystem(SystemBase):
    '''GPU resource management. If something requires GPU resources (eg shaders, buffers, textures), then it requires management and clenaup.
    This system tacks all GpuResource objects and is responsible for telling said objects to acquire their resources or release them'''

    def __init__(self):
        super().__init__()
        self.active_resources: List[GpuResource] = []
        self.pending_acquires: List[GpuResource] = []
        self.gpu_available = False 
        self.try_to_acquire = True #used to flag resource release when

    def v_init_system(self):
        # window system is now gauranteed to be instantiated
        from .WindowSystem import WindowSystem, get_window_system
        win_sys:WindowSystem = get_window_system()
        win_sys.event_gpu_resources_changed.add_subscriber(self._handle_gpu_ready_changed)

    def v_shutdown_system(self):
        self._release_active_resources()

    def v_tick_system(self, dt_sec:float):
        if self.gpu_available and self.try_to_acquire:
            self._acquire_pending_resources()
        else:
            self._release_active_resources()

    def _handle_gpu_ready_changed(self, args)->None:
        from .WindowSystem import EventArgs_GpuResourceChanged
        typed_args:EventArgs_GpuResourceChanged = args #avoiding adding type to parameter as dont want to create circular dependency on systems

        self.gpu_available = typed_args.gpu_ready
        # set up GPU ready flag before actually attempting to acquire resources; can't acquire resources if no gpu availble
        for resource in self.active_resources:
            resource.is_gpu_available = typed_args.gpu_ready
        for pending_resource in self.pending_acquires:
            pending_resource.is_gpu_available = typed_args.gpu_ready
        # note: dont acquire resources here, let the tick do it for simple design

    def _acquire_pending_resources(self):
        for new_resource in self.pending_acquires:
            new_resource._acquire_resources()
            self.active_resources.append(new_resource)
        self.pending_acquires.clear()

    def _release_active_resources(self):
        for active_resource in self.active_resources:
            active_resource._release_resources()
            self.pending_acquires.append(active_resource)

    def _add(self, resource: GpuResource):
        ''' Should be called automatically and internally by the GPUResource, should never need to call this externally'''
        if (resource is not None
        and resource not in self.active_resources 
        and resource not in self.pending_acquires):
            resource.is_gpu_available = self.gpu_available
            self.pending_acquires.append(resource)



#hack to get the tests to see import
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from src.EnginePkg.EventObject import Event

class _TestEventObject:
    def __init__(self) -> None:
        super().__init__()
        self.num_handles:int = 0
    def handler(self, args):
        self.num_handles = self.num_handles + 1

def test_add_subscription():
    obj:_TestEventObject = _TestEventObject()

    event:Event = Event()
    event.add_subscriber(obj.handler)

    event.broadcast()

    assert obj.num_handles == 1

def test_removal():
    obj:_TestEventObject = _TestEventObject()

    event:Event = Event()
    event.add_subscriber(obj.handler)
    event.broadcast()
    event.remove_subscriber(obj.handler)
    event.broadcast()

    #should not increment twice because was removed
    assert obj.num_handles == 1

def test_none_static():
    obj:_TestEventObject = _TestEventObject()
    event:Event = Event()
    event.add_subscriber(obj.handler)

    event2:Event = Event()
    event2.add_subscriber(obj.handler)

    assert len(event._subscribers) == 1
    assert len(event2._subscribers) == 1


class _TestEvent_SelfSubscriptions:
    def __init__(self) -> None:
        super().__init__()
        self.event:Event = None
        self.bind_to_event_again = False
        self.remove_from_event = False
        self.many_add_removes_test = False
    def handle_first(self, args):
        if self.bind_to_event_again:
            self.event.add_subscriber(self.handle_first)
        if self.remove_from_event:
            self.event.remove_subscriber(self.handle_first)
        if self.many_add_removes_test:
            self.event.add_subscriber(self.handle_first)    #+2
            self.event.remove_subscriber(self.handle_first) #+1
            self.event.remove_subscriber(self.handle_first) #0
            self.event.add_subscriber(self.handle_first)    #+1

def test_removal_during_broadcast():
    obj:_TestEvent_SelfSubscriptions = _TestEvent_SelfSubscriptions()
    event:Event = Event()

    event.add_subscriber(obj.handle_first)
    obj.remove_from_event = True
    obj.event = event

    event.broadcast()

    assert len(event._subscribers) == 0

def test_add_during_broadcast():
    obj:_TestEvent_SelfSubscriptions = _TestEvent_SelfSubscriptions()
    event:Event = Event()

    event.add_subscriber(obj.handle_first)
    obj.bind_to_event_again = True
    obj.event = event

    event.broadcast()

    assert len(event._subscribers) == 2

def test_broadcast_many_add_removes():
    obj:_TestEvent_SelfSubscriptions = _TestEvent_SelfSubscriptions()
    event:Event = Event()

    event.add_subscriber(obj.handle_first)
    obj.many_add_removes_test = True
    obj.event = event

    event.broadcast()

    assert len(event._subscribers) == 1


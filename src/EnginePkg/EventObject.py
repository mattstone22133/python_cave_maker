
# there is probably a more pythonic way to do this, but this matches c# multicast delegate pattern
from typing import Callable, List, Set

class Event:
    '''A class that allows binding callbacks to event objects. 
        subscribers are considered strong references, and should be manually removed.
            Making them weakref has unfortunately result of not being able to just pass callbacks like event.add_subscriber(obj.callback)
            as the bound function will be deleted after add_subscriber goes out of scope.
            to stop dead on arrivale using weakrefs, something like this may be useful to investigate: weakref.WeakMethod or custom code https://code.activestate.com/recipes/81253/
        when changing this class, be sure to run tests in test_events.py and add new tests for new features'''
    def __init__(self, reflection_event_args=None) -> None:
        super().__init__()
        self._subscribers:List[Callable] = []
        self._broadcasting:bool = False
        self._pending_add_subscribers: Set[Callable] = set()
        self._pending_removals: Set[Callable] = set()
        self.reflection_event_args = reflection_event_args # note: does not enforce what users broadcast, perhaps useful for runtime querying

    def add_subscriber(self, subscriber:Callable):
        if not self._broadcasting:
            self._subscribers.append(subscriber)
        elif subscriber in self._pending_removals:
            self._pending_removals.remove(subscriber)
        else:
            self._pending_add_subscribers.add(subscriber)
        handle = subscriber
        return handle

    def remove_subscriber(self, subscriber:Callable):
        if not self._broadcasting:
            for current_sub in self._subscribers:
                if current_sub == subscriber or current_sub is subscriber: #must check == to support removal by function name
                    self._subscribers.remove(current_sub)
                    break #removed first occurance, leave remaining to allow even subscription stacking
        elif subscriber in self._pending_add_subscribers:
            self._pending_add_subscribers.remove(subscriber)
        else:
            self._pending_removals.add(subscriber)
    def __len__(self):
        return len(self._subscribers) + len(self._pending_add_subscribers) - len(self._pending_removals)

    def broadcast(self, event_args=None):
        '''Broadcasts the event to all subscribers'''
        self._broadcasting = True
        for subscriber in self._subscribers:
            subscriber(event_args)
        self._broadcasting = False

        for new_subscriber in self._pending_add_subscribers:
            self.add_subscriber(new_subscriber)

        for remove_subscriber in self._pending_removals:
            self.remove_subscriber(remove_subscriber)

        self._pending_removals.clear()
        self._pending_add_subscribers.clear()



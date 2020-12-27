
#there is probably a more pythonic way to do this, but this matches c# multicast delegate pattern
from typing import Callable, List, Set

class Event:
    def __init__(self) -> None:
        super().__init__()

        self._subscribers:List[Callable] = []
        self._broadcasting:bool = False
        self._pending_add_subscribers: Set[Callable] = set()
        self._pending_removals: Set[Callable] = set()

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

    def broadcast(self, event_args=[]):
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



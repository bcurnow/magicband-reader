
from enum import Enum, auto
from importlib import import_module
from pkgutil import iter_modules


class EventType(Enum):
    NONE = auto()
    AUTHORIZED = auto()
    UNAUTHORIZED = auto()

class AbstractHandler():
    def __init__(self, priority=100):
        self.priority = priority
        self._method_map = {
            EventType.NONE: self.handle_none_event,
            EventType.AUTHORIZED: self.handle_authorized_event,
            EventType.UNAUTHORIZED: self.handle_unauthorized_event,
        }

    def handle_event(self, event, event_type):
        """ Method called to handle an event, this method delegates to the handle_*_event methods as appropriate."""
        self._method_map[event_type](event)

    def handle_authorized_event(self, event):
        """ Called when authorization for an event has succeeded."""
        pass

    def handle_unauthorized_event(self, event):
        """ Called when authorization for an event has failed."""
        pass

    def handle_none_event(self, event):
        """ Called when reading an event returns None. This isn't supposed to happen and should be considered exceptional."""
        pass


def register_handlers(ctx):
    """ Find all the modules in the specified package and register their 'handle_event' methods as event handlers."""
    import magicbandreader.handlers as pkg
    rv = []

    for module_info in iter_modules(path=pkg.__path__):
        module = import_module(f'{pkg.__name__}.{module_info.name}')
        register_method = getattr(module, 'register', None)
        if register_method:
            rv.append(register_method(ctx))

    return sorted(rv, key=lambda h: h.priority)

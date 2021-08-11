from importlib import import_module
import logging
from pkgutil import iter_modules

from magicbandreader.event import EventType


class AbstractHandler():
    def __init__(self, priority=100):
        self.priority = priority
        self._method_map = {
            EventType.NONE: self.handle_none_event,
            EventType.AUTHORIZED: self.handle_authorized_event,
            EventType.UNAUTHORIZED: self.handle_unauthorized_event,
        }

    def handle_event(self, event):
        """ Method called to handle an event, this method delegates to the handle_*_event methods as appropriate."""
        logging.debug(f'Received an event of type {event.type}')
        if event.type:
            self._method_map[event.type](event)
        else:
            logging.warn((
                f'handle_event called on {self.__class__.__name__} (priority: {self.priority}) but the event has no type. ',
                'Please check the priority order of the handlers.'
                ))

    def handle_authorized_event(self, event):
        """ Called when authorization for an event has succeeded."""
        logging.debug(f'Processing an authorized event within the AbstractHandler')

    def handle_unauthorized_event(self, event):
        """ Called when authorization for an event has failed."""
        logging.debug(f'Processing an unauthorized event within the AbstractHandler')

    def handle_none_event(self, event):
        """ Called when reading an event returns None. This isn't supposed to happen and should be considered exceptional."""
        logging.debug(f'Processing a none event within the AbstractHandler (this should not be possible!)')


def register_handlers(ctx):
    """ Find all the modules in the specified package and register their 'handle_event' methods as event handlers."""
    import magicbandreader.handlers as pkg
    rv = []

    for module_info in iter_modules(path=pkg.__path__):
        module = import_module(f'{pkg.__name__}.{module_info.name}')
        logging.debug(f'Found handler {module_info.name} in package {pkg.__name__}')
        register_method = getattr(module, 'register', None)
        if register_method:
            logging.debug(f'Found register method for handler {module_info.name} in package {pkg.__name__}')
            rv.append(register_method(ctx))

    return sorted(rv, key=lambda h: h.priority)

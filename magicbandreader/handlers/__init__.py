
from importlib import import_module
from pkgutil import iter_modules

import magicbandreader.handlers as pkg

EVENT_METHOD_AUTHORIZED = 'handle_authorized_event'
EVENT_METHOD_UNAUTHORIZED = 'handle_unauthorized_event'
EVENT_METHOD_NONE = 'handle_none_event'

def register_handlers():
    """ Find all the modules in the specified package and register their 'handle_event' methods as event handlers."""
    rv = {
        EVENT_METHOD_AUTHORIZED: [],
        EVENT_METHOD_UNAUTHORIZED: [],
        EVENT_METHOD_NONE: [],
    }

    for module_info in iter_modules(path=pkg.__path__):
        module = import_module(f'{pkg.__name__}.{module_info.name}')
        for method_name, handlers in rv.items():
            method = getattr(module, method_name, None)
            if method:
                handlers.append(method)
    return rv

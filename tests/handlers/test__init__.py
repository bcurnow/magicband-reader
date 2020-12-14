import importlib
import os
import pkgutil
import sys

from unittest.mock import patch

from magicbandreader.event import Event, EventType
from magicbandreader.handlers import AbstractHandler, register_handlers


class FakeHandler(AbstractHandler):
    def handle_authorized_event(self, event):
        self.handle_authorized_event_called = (event,)

    def handle_unauthorized_event(self, event):
        self.handle_unauthorized_event_called = (event,)

    def handle_none_event(self, event):
        self.handle_none_event_called = (event,)


def test_AbstractHandler__init__():
    ah = AbstractHandler(400)
    assert ah.priority == 400
    assert ah._method_map == {
        EventType.NONE: ah.handle_none_event,
        EventType.AUTHORIZED: ah.handle_authorized_event,
        EventType.UNAUTHORIZED: ah.handle_unauthorized_event,

    }


def test_AbstractHandler_handle_authorized_event():
    # Call the real one, it's an empty method so it should never throw and exception
    # and this ensures coverage
    AbstractHandler().handle_authorized_event(None)
    h = FakeHandler()
    e = Event(None, {}, type=EventType.AUTHORIZED)
    h.handle_event(e)
    print(dir(h))
    assert h.handle_authorized_event_called == (e,)


def test_AbstractHandler_handle_unauthorized_event():
    # Call the real one, it's an empty method so it should never throw and exception
    # and this ensures coverage
    AbstractHandler().handle_unauthorized_event(None)
    h = FakeHandler()
    e = Event(None, {}, type=EventType.UNAUTHORIZED)
    h.handle_event(e)
    assert h.handle_unauthorized_event_called == (e,)


def test_AbstractHandler_handle_none_event():
    # Call the real one, it's an empty method so it should never throw and exception
    # and this ensures coverage
    AbstractHandler().handle_none_event(None)
    h = FakeHandler()
    e = Event(None, {}, type=EventType.NONE)
    h.handle_event(e)
    assert h.handle_none_event_called == (e,)


@patch('magicbandreader.handlers.logging')
def test_AbstractHandler_handle_event_notype(logging):
    h = FakeHandler(priority=1)
    e = Event(None, {}, type=None)
    h.handle_event(e)
    logging.warn.assert_called_once_with(('handle_event called on FakeHandler (priority: 1) but the event has no type. ',
                                         'Please check the priority order of the handlers.'))


@patch('magicbandreader.handlers.import_module')
@patch('magicbandreader.handlers.iter_modules')
def test_register_handlers(iter_modules, import_module):
    testhandlers = _import_testhandlers()
    import testhandlers.one
    import testhandlers.two
    import testhandlers.three
    import testhandlers.not_a_handler
    iter_modules.return_value = pkgutil.iter_modules(path=testhandlers.__path__)
    import_module.side_effect = [testhandlers.one,
                                 testhandlers.two,
                                 testhandlers.three,
                                 testhandlers.not_a_handler,
                                 ]
    handlers = register_handlers(None)

    assert len(handlers) == 3
    # The handlers should be in priority order, not iteration or lexical order
    for i, typ in enumerate([
        testhandlers.three.ThreeHandler,
        testhandlers.two.TwoHandler,
        testhandlers.one.OneHandler,
    ]):
        assert isinstance(handlers[i], typ)


def _import_testhandlers():
    # Because of the way python works, we need to do a bit of trickery to make the testhandlers package available
    # First, determine the absolute path to the testhandlers directory
    module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'testhandlers'))

    # Import the __init__.py file as a module to serve as the package
    package = _load_from_path('testhandlers', os.path.join(module_path, '__init__.py'))

    return package


def _load_from_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

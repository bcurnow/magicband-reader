from http.server import BaseHTTPRequestHandler
import threading
from unittest.mock import patch, Mock

import pytest

from magicbandreader.router import Router, RFIDServer, RFIDRequestHandler


@patch('magicbandreader.router.HTTPServer.__init__')
@patch('magicbandreader.router.logging')
@patch('magicbandreader.router.threading')
def test_Router___init__(threading, logging, HTTPServer, context):
    t = threading.Thread.return_value
    router = Router(context)
    assert router.ctx == context
    assert router.uid_request is not None
    assert router.uid_ready is not None
    assert isinstance(router.server, RFIDServer)
    threading.Thread.assert_called_once_with(target=router.server.serve_forever, name='HTTPListener-Thread', daemon=True)
    assert router.listener_thread is t
    logging.info.assert_called_once_with(f'Starting server at localhost:{context.port_number}')
    t.start.assert_called_once


@pytest.mark.parametrize(
    ('uid_request'),
    [
        (True),
        (False),
    ],
    ids=[
        'Server requested uid',
        'Server did not request uid',
    ]
    )
@patch('magicbandreader.router.HTTPServer.__init__')
@patch('magicbandreader.router.logging')
@patch('magicbandreader.router.threading')
def test_Router_route(threading, logging, HTTPServer, context, uid_request, none_event):
    handler1 = Mock()
    handler2 = Mock()
    context.handlers = [handler1, handler2]
    router = Router(context)
    server = Mock()
    router.server = server
    router.uid_request.is_set.return_value = uid_request

    router.route(none_event)
    if uid_request:
        logging.debug.assert_called_once_with('uid_request event is set, sending uid to the web endpoint')
        router.uid_request.clear.assert_called_once()
        server.set_uid.assert_called_once_with(none_event.id)
    else:
        logging.debug.assert_called_once_with('uid_request event is not set, sending uid to the handlers')
        handler1.handle_event.assert_called_once_with(none_event)
        handler2.handle_event.assert_called_once_with(none_event)


@patch('magicbandreader.router.HTTPServer.__init__')
def test_RFIDServer___init__(HTTPServer):
    uid_request = Mock(spec=threading.Event)
    uid_ready = Mock(spec=threading.Event)
    server = RFIDServer(('localhost', 8080), RFIDRequestHandler, uid_ready, uid_request)
    HTTPServer.assert_called_once_with(('localhost', 8080), RFIDRequestHandler)
    assert server.uid_ready == uid_ready
    assert server.uid_request == uid_request


@patch('magicbandreader.router.HTTPServer.__init__')
def test_RFIDServer_set_uid(HTTPServer):
    uid_request = Mock(spec=threading.Event)
    uid_ready = Mock(spec=threading.Event)
    server = RFIDServer(('localhost', 8080), RFIDRequestHandler, uid_ready, uid_request)
    server.set_uid('test')
    assert server.uid == 'test'
    uid_ready.set.assert_called_once()


@patch('magicbandreader.router.HTTPServer.__init__')
def test_RFIDServer_get_uid(HTTPServer):
    uid_request = Mock(spec=threading.Event)
    uid_ready = Mock(spec=threading.Event)
    server = RFIDServer(('localhost', 8080), RFIDRequestHandler, uid_ready, uid_request)
    server.set_uid('test')
    uid = server.get_uid()
    assert uid == 'test'
    assert server.uid is None
    uid_ready.clear.assert_called_once()


class MockRFIDRequestHandler(RFIDRequestHandler):
    """ I don't want to spend time mocking out the internals of http.server so I'm just going to skip all the init."""
    def __init__(self, path='/get_uid', uid='testuid'):
        self.path = path
        self.server = Mock(spec=RFIDServer)
        self.server.uid_request = Mock(spec=threading.Event)
        self.server.uid_ready = Mock(spec=threading.Event)
        self.server.get_uid.return_value = uid
        self.base_http_request_handler = Mock(spec=BaseHTTPRequestHandler)
        self.wfile = Mock(name='wfile')
        self.requestline = 'Testing request, not used'
        self.client_address = ['unused']
        self.request_version = 'unused'

    def send_response(self, response):
        self.base_http_request_handler.send_response(response)

    def send_header(self, name, value):
        self.base_http_request_handler.send_header(name, value)

    def end_headers(self):
        self.base_http_request_handler.end_headers()

    def send_error(self, code, explain=None):
        # The below will help the test code be more true to the real code
        if explain:
            self.base_http_request_handler.send_error(code, explain=explain)
        else:
            self.base_http_request_handler.send_error(code)

    def log_date_time_string(self):
        """ Always return the same data and time string to ease testing."""
        return '10/Jan/2021 16:18:54'


def test_RFIDRequestHandler_version_string():
    rh = MockRFIDRequestHandler()
    assert rh.version_string() == 'MagicBand Reader HTTP Server'


@patch('magicbandreader.router.logging')
def test_RFIDRequestHandler_log_message(logging):
    rh = MockRFIDRequestHandler()
    rh.log_message('%s', 'test')
    logging.info.assert_called_once_with('unused - - [10/Jan/2021 16:18:54] test\n')


@pytest.mark.parametrize(
    ('path', 'timeout', 'uid_ready_event', 'uid'),
    [
        ('/unknown', None, None, None),
        ('/get_uid', None, False, None),
        ('/get_uid', None, True, None),
        ('/get_uid', None, True, 'testuid'),
        ('/get_uid', 25, True, 'testuid'),
    ],
    ids=[
        'Invalid URL (404)',
        'Timeout (408)',
        'Bad UID (500)',
        'Success (200)',
        'Success with custom timeout (200)',
    ]
    )
def test_RFIDRequestHandler_doGET(path, timeout, uid_ready_event, uid):
    rh = MockRFIDRequestHandler(to_path(path, timeout), uid)
    rh.server.uid_ready.wait.return_value = uid_ready_event
    rh.do_GET()
    if path != '/get_uid':
        rh.base_http_request_handler.send_error.assert_called_once_with(404, explain=f'No mapping for {path}')
    else:
        rh.server.uid_request.set.assert_called_once()
        if timeout:
            rh.server.uid_ready.wait.assert_called_once_with(timeout)
        else:
            rh.server.uid_ready.wait.assert_called_once_with(10 * 60)

        if uid_ready_event:
            if uid:
                rh.base_http_request_handler.send_response.assert_called_once_with(200)
                rh.base_http_request_handler.send_header.assert_called_once_with('Content-type', 'text/plain')
                rh.base_http_request_handler.end_headers.assert_called_once()
                rh.wfile.write.assert_called_once_with(uid.encode())
        else:
            rh.base_http_request_handler.send_error.assert_called_once_with(408)

        rh.server.uid_request.clear.assert_called_once()


def to_path(path, timeout):
    if timeout:
        return ''.join([path, '?', 'timeout=', str(timeout)])

    return path

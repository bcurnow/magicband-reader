import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from urllib.parse import urlparse, parse_qs


class Router:
    def __init__(self, ctx):
        self.ctx = ctx
        self.uid_request = threading.Event()
        self.uid_ready = threading.Event()
        self.server = RFIDServer(('localhost', ctx.port_number), RFIDRequestHandler, self.uid_ready, self.uid_request)
        t = threading.Thread(
            target=self.server.serve_forever,
            name='HTTPListener-Thread',
            daemon=True
            )
        self.listener_thread = t
        logging.info(f'Starting server at localhost:{ctx.port_number}')
        t.start()

    def route(self, event):
        if self.uid_request.is_set():
            logging.debug('uid_request event is set, sending uid to the web endpoint')
            # Reset the event
            self.uid_request.clear()
            # There has been a request for a uid, direct this UID to the server
            self.server.set_uid(event.id)
        else:
            logging.debug('uid_request event is not set, sending uid to the handlers')
            for handler in self.ctx.handlers:
                handler.handle_event(event)


class RFIDServer(HTTPServer):
    def __init__(self, server_address, request_handler_class, uid_ready, uid_request):
        super().__init__(server_address, request_handler_class)
        self.uid_ready = uid_ready
        self.uid_request = uid_request

    def set_uid(self, uid):
        self.uid = uid
        self.uid_ready.set()

    def get_uid(self):
        rv = self.uid
        self.uid = None
        self.uid_ready.clear()
        return rv


class RFIDRequestHandler(BaseHTTPRequestHandler):
    def version_string(self):
        return 'MagicBand Reader HTTP Server'

    def log_message(self, format, *args):
        logging.info(f'{self.address_string()} - - [{self.log_date_time_string()}] {format%args}\n')

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == '/get_uid':
            # Let the router know we need the next event
            try:
                self.server.uid_request.set()
                # Parse the query to see if there's a specified timeout
                params = parse_qs(url.query)
                if 'timeout' in params:
                    timeout = int(params['timeout'][0])
                else:
                    # Set the timeout to 10 minutes maximum
                    timeout = 10 * 60
                # Wait for the uid to be ready
                if self.server.uid_ready.wait(timeout):
                    uid = self.server.get_uid()
                    if uid:
                        self.send_response(200)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(uid.encode())
                    else:
                        self.send_error(500, explain=f'uid of {uid} returned')
                else:
                    self.send_error(408)
            finally:
                # No matter what happens, we need to clear the uid_request event or all future readers
                # will come here
                self.server.uid_request.clear()
        else:
            self.send_error(404, explain=f'No mapping for {url.path}')

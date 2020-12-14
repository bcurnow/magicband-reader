import logging
from urllib.parse import urljoin, quote

import requests


class RfidSecuritySvcAuthorizer:
    """ Uses the rfid-security-svc to authorize an rfid_id for a named permission. """
    def __init__(self, ctx):
        self.headers = {'X-RFIDSECURITYSVC-API-KEY': quote(ctx.api_key)}
        self.api_ssl_verify = ctx.api_ssl_verify
        self.permission = ctx.permission
        self.url = urljoin(ctx.api_url, f'authorized/media/{{}}/perm/{quote(self.permission)}')

    def authorized(self, rfid_id):
        """
        Checks the supplied event against the rfid-security-svc to see if it is authorized.
        Returns True if authorized.
        Returns False otherwise.
        """
        url = self.url.format(rfid_id)
        try:
            response = requests.get(
                url,
                headers=self.headers,
                verify=self.api_ssl_verify
                )
            if response.status_code != 200 and response.status_code != 403:
                logging.error(f'Unexpected status code back from {url}: {response.status_code}')
            return response.status_code == 200
        except requests.ConnectionError as e:
            logging.error(f'Unable to connect to {url}: {e}.')
            return False

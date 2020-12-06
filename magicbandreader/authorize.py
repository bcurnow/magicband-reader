import logging
from urllib.parse import urljoin, quote

import requests


class RfidSecuritySvcAuthorizer:
    """ Uses the rfid-security-svc to authorize an rfid_id for a named permission. """
    def __init__(self, api_url, api_key, api_ssl_verify=True, permission='Open Door'):
        self.api_url = api_url
        self.api_key = api_key
        self.api_ssl_verify = api_ssl_verify
        self.permission = permission
        self.url = urljoin(api_url, f'authorized/media/{{}}/perm/{quote(permission)}')

    def authorized(self, rfid_id):
        """
        Checks the supplied event against the rfid-security-svc to see if it is authorized.
        Returns True if authorized.
        Returns False otherwise.
        """
        try:
            response = requests.get(
                self.url.format(rfid_id),
                headers={'X-RFIDSECURITYSVC-API-KEY': quote(self.api_key)},
                verify=self.api_ssl_verify
                )
            if response.status_code != 200 and response.status_code != 403:
                logging.error(f'Unexpected status code back from {self.url.format(rfid_id)}: {response.status_code}')
            return response.status_code == 200
        except requests.exceptions.ConnectionError as e:
            logging.error(f'Unable to connect to {self.url.format(rfid_id)}: {e}.')
            return False

import logging
from urllib.parse import urljoin, quote

import requests


class RfidSecuritySvcAuthorizer:
    """ Uses the rfid-security-svc to authorize an rfid_id for a named permission. """
    def __init__(self, api_url, api_key, permission='Open Door'):
        self.api_url = api_url
        self.api_key = api_key
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
                verify=False
                )
            return response.status_code == 200
        except requests.exceptions.ConnectionError as e:
            logging.error(f'Unable to connect to {self.url.format(rfid_id)}: {e}.')
            return False

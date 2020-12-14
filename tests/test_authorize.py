import requests
from types import SimpleNamespace
from urllib.parse import urljoin, quote

import pytest
from unittest.mock import patch, PropertyMock

from magicbandreader.authorize import RfidSecuritySvcAuthorizer


CONFIG = {
    'api_key': 'test key / & with space',
    'api_url': 'test://testing.test',
    'api_ssl_verify': 'sounds like a good idea',
    'permission': 'Test',
}


CTX = SimpleNamespace(**CONFIG)


def test__init__():
    auth = RfidSecuritySvcAuthorizer(CTX)
    assert auth.headers == {'X-RFIDSECURITYSVC-API-KEY': quote(CTX.api_key)}
    assert auth.api_ssl_verify == CTX.api_ssl_verify
    assert auth.permission == CTX.permission
    assert auth.url == urljoin(CTX.api_url, f'authorized/media/{{}}/perm/{quote(CTX.permission)}')


@pytest.mark.parametrize(
    ('error', 'status_code'),
    [
        (None, 200),
        (None, 403),
        (None, 501),
        (requests.ConnectionError('Testing'), None),
    ]
    )
@patch('magicbandreader.authorize.logging')
@patch('magicbandreader.authorize.requests.get')
def test_authorized(get, logging, error, status_code):
    response = get.return_value
    mock_status_code = PropertyMock(name='status_code', return_value=status_code)
    type(response).status_code = mock_status_code
    if error:
        get.side_effect = error
    authorizer = RfidSecuritySvcAuthorizer(CTX)
    url = authorizer.url.format('test_id')

    ret = authorizer.authorized('test_id')
    if error:
        logging.error.assert_called_once_with(f'Unable to connect to {url}: Testing.')
    else:
        if status_code != 200 and status_code != 403:
            logging.error.assert_called_once_with(f'Unexpected status code back from authorized/media/test_id/perm/Test: {status_code}')

    assert ret == (status_code == 200)
    get.assert_called_once_with(url, headers=authorizer.headers, verify=authorizer.api_ssl_verify)

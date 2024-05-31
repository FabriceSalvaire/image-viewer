####################################################################################################
#
# ... — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['RequestManager', 'Request', 'Url']

####################################################################################################

from pathlib import Path
from typing import Union
from urllib.parse import urlparse, parse_qs, urlencode
import logging

# [Requests documentation](https://requests.readthedocs.io/en/latest)
import requests
# [How could I use requests in asyncio? - Stack Overflow](https://stackoverflow.com/questions/22190403/how-could-i-use-requests-in-asyncio)
# [curl_cffi documentation](https://curl-cffi.readthedocs.io/en/latest/)

####################################################################################################

_module_logger = logging.getLogger(__name__)

type PathStr = Union[Path, str]

SAFE_URL = '|'

####################################################################################################

class Url:

    ##############################################

    def __init__(self, url: str, params: dict = {}) -> None:
        self._url = str(url)
        self._params = dict(params)

    ##############################################

    def __str__(self) -> str:
        if self._params:
            return self._url + '?' + urlencode(self._params, safe=SAFE_URL)
        else:
            return self._url

####################################################################################################

class Request:

    _logger = _module_logger.getChild('Request')

    ##############################################

    def __init__(
        self,
        manager: 'RequestManager',
        urlp: str = None,
        url: str = None,
        params: dict = None,
        headers: dict = None,
        cookies: dict = None,
    ) -> None:
        self._manager = manager
        if params:
            self._urlp = str(urlp)
            self._url = str(url)
            self._params = dict(params)
        else:
            self._urlp = str(urlp)
            _ = urlparse(self._urlp)
            self._params = parse_qs(_.query)
            self._url = _._replace(query=None).geturl()
        # Fixme: case dict(headers) ?
        self._headers = headers or {}
        self._cookies = cookies or {}

    ##############################################

    def perform(self) -> bytes:
        self._logger.info(f'Get {self._urlp}')
        r = requests.get(
            self._url,
            params=self._params,
            headers=self._headers,
            cookies=self._cookies,
            # timeout
        )
        if r.ok:
            # Payload(r.content, r.headers['content-type'])
            type_ = r.headers['content-type']
            # self._logger.info(f'Payload is {type_}')
            # r.content can be encoded in any charset
            if type_ in ('image/jpeg'):
                return r.content
            else:
                return r.text.encode('utf8')
        else:
            self._logger.error(f'Get for {self._urlp} failed with {r.status_code} {r.text}')
            raise NameError(f'Get Failure')

####################################################################################################

class RequestManager:

    _logger = _module_logger.getChild('RequestManager')

    ##############################################

    def __init__(self) -> None:
        pass

    ##############################################

    def get(self, *args, **kwargs) -> bytes:
        _ = Request(self, *args, **kwargs)
        return _.perform()

    ##############################################

    def _save_binary(self, path: str | Path, data: bytes) -> None:
        with open(path, 'wb') as fh:
            fh.write(data)

    ##############################################

    def save_binary(self, url: str, path: str | Path):
        path = Path(path)
        if path.exists():
            self._logger.warning(f"{path} exists")
            # raise NameError()
        else:
            self._logger.info(f"GET {url} -> {path}")
            req = Request(self, urlp=url)
            _ = req.perform()
            self._save_binary(path, _)

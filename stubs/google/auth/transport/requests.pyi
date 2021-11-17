from typing import Any

import requests.exceptions
from google.auth import environment_vars as environment_vars
from google.auth import exceptions as exceptions
from google.auth import transport as transport
from google.oauth2 import service_account as service_account

class _Response(transport.Response):
    def __init__(self, response) -> None: ...
    @property
    def status(self): ...
    @property
    def headers(self): ...
    @property
    def data(self): ...

class TimeoutGuard:
    remaining_timeout: Any
    def __init__(self, timeout, timeout_error_type=...) -> None: ...
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_value, traceback) -> None: ...

class Request(transport.Request):
    session: Any
    def __init__(self, session: Any | None = ...) -> None: ...
    def __call__(
        self,
        url,
        method: str = ...,
        body: Any | None = ...,
        headers: Any | None = ...,
        timeout=...,
        **kwargs
    ): ...

class _MutualTlsAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, cert, key) -> None: ...
    def init_poolmanager(self, *args, **kwargs) -> None: ...
    def proxy_manager_for(self, *args, **kwargs): ...

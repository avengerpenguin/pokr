import wsgiref.simple_server
import wsgiref.util
from typing import Any

class Flow:
    client_type: Any
    client_config: Any
    oauth2session: Any
    code_verifier: Any
    autogenerate_code_verifier: Any
    def __init__(
        self,
        oauth2session,
        client_type,
        client_config,
        redirect_uri: Any | None = ...,
        code_verifier: Any | None = ...,
        autogenerate_code_verifier: bool = ...,
    ) -> None: ...
    @classmethod
    def from_client_config(cls, client_config, scopes, **kwargs): ...
    @classmethod
    def from_client_secrets_file(
        cls, client_secrets_file, scopes, **kwargs
    ): ...
    @property
    def redirect_uri(self): ...
    @redirect_uri.setter
    def redirect_uri(self, value) -> None: ...
    def authorization_url(self, **kwargs): ...
    def fetch_token(self, **kwargs): ...
    @property
    def credentials(self): ...
    def authorized_session(self): ...

class InstalledAppFlow(Flow):
    redirect_uri: Any
    def run_console(
        self,
        authorization_prompt_message=...,
        authorization_code_message=...,
        **kwargs
    ): ...
    def run_local_server(
        self,
        host: str = ...,
        port: int = ...,
        authorization_prompt_message=...,
        success_message=...,
        open_browser: bool = ...,
        redirect_uri_trailing_slash: bool = ...,
        **kwargs
    ): ...

class _WSGIRequestHandler(wsgiref.simple_server.WSGIRequestHandler):
    def log_message(self, format, *args) -> None: ...

class _RedirectWSGIApp:
    last_request_uri: Any
    def __init__(self, success_message) -> None: ...
    def __call__(self, environ, start_response): ...

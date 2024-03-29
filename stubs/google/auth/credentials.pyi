import abc
from typing import Any

class Credentials(metaclass=abc.ABCMeta):
    token: Any
    expiry: Any
    def __init__(self) -> None: ...
    @property
    def expired(self): ...
    @property
    def valid(self): ...
    @property
    def quota_project_id(self): ...
    @abc.abstractmethod
    def refresh(self, request): ...
    def apply(self, headers, token: Any | None = ...) -> None: ...
    def before_request(self, request, method, url, headers) -> None: ...

class CredentialsWithQuotaProject(Credentials, metaclass=abc.ABCMeta):
    def with_quota_project(self, quota_project_id) -> None: ...

class AnonymousCredentials(Credentials):
    @property
    def expired(self): ...
    @property
    def valid(self): ...
    def refresh(self, request) -> None: ...
    def apply(self, headers, token: Any | None = ...) -> None: ...
    def before_request(self, request, method, url, headers) -> None: ...

class ReadOnlyScoped(metaclass=abc.ABCMeta):
    def __init__(self) -> None: ...
    @property
    def scopes(self): ...
    @property
    def default_scopes(self): ...
    @property
    @abc.abstractmethod
    def requires_scopes(self): ...
    def has_scopes(self, scopes): ...

class Scoped(ReadOnlyScoped, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def with_scopes(self, scopes, default_scopes: Any | None = ...): ...

def with_scopes_if_required(
    credentials, scopes, default_scopes: Any | None = ...
): ...

class Signing(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def sign_bytes(self, message): ...
    @property
    @abc.abstractmethod
    def signer_email(self): ...
    @property
    @abc.abstractmethod
    def signer(self): ...

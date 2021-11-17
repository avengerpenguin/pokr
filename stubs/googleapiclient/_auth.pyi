from typing import Any

HAS_GOOGLE_AUTH: bool
HAS_OAUTH2CLIENT: bool

def credentials_from_file(
    filename, scopes: Any | None = ..., quota_project_id: Any | None = ...
): ...
def default_credentials(
    scopes: Any | None = ..., quota_project_id: Any | None = ...
): ...
def with_scopes(credentials, scopes): ...
def authorized_http(credentials): ...
def refresh_credentials(credentials): ...
def apply_credentials(credentials, headers): ...
def is_valid(credentials): ...
def get_credentials_from_http(http): ...

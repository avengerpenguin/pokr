from email.generator import BytesGenerator
from typing import Any

class _BytesGenerator(BytesGenerator): ...

def fix_method_name(name): ...
def key2param(key): ...
def build(
    serviceName,
    version,
    http: Any | None = ...,
    discoveryServiceUrl: Any | None = ...,
    developerKey: Any | None = ...,
    model: Any | None = ...,
    requestBuilder=...,
    credentials: Any | None = ...,
    cache_discovery: bool = ...,
    cache: Any | None = ...,
    client_options: Any | None = ...,
    adc_cert_path: Any | None = ...,
    adc_key_path: Any | None = ...,
    num_retries: int = ...,
    static_discovery: Any | None = ...,
    always_use_jwt_access: bool = ...,
): ...
def build_from_document(
    service,
    base: Any | None = ...,
    future: Any | None = ...,
    http: Any | None = ...,
    developerKey: Any | None = ...,
    model: Any | None = ...,
    requestBuilder=...,
    credentials: Any | None = ...,
    client_options: Any | None = ...,
    adc_cert_path: Any | None = ...,
    adc_key_path: Any | None = ...,
    always_use_jwt_access: bool = ...,
): ...

class ResourceMethodParameters:
    argmap: Any
    required_params: Any
    repeated_params: Any
    pattern_params: Any
    query_params: Any
    path_params: Any
    param_types: Any
    enum_params: Any
    def __init__(self, method_desc) -> None: ...
    def set_parameters(self, method_desc) -> None: ...

class Resource:
    def __init__(
        self,
        http,
        baseUrl,
        model,
        requestBuilder,
        developerKey,
        resourceDesc,
        rootDesc,
        schema,
    ) -> None: ...
    def __enter__(self): ...
    def __exit__(self, exc_type, exc, exc_tb) -> None: ...
    def close(self) -> None: ...

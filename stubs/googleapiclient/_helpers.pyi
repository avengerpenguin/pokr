from typing import Any

logger: Any
POSITIONAL_WARNING: str
POSITIONAL_EXCEPTION: str
POSITIONAL_IGNORE: str
POSITIONAL_SET: Any
positional_parameters_enforcement = POSITIONAL_WARNING

def positional(max_positional_args): ...
def parse_unique_urlencoded(content): ...
def update_query_params(uri, params): ...

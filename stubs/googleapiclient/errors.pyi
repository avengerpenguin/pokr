from typing import Any

class Error(Exception): ...

class HttpError(Error):
    resp: Any
    content: Any
    uri: Any
    error_details: str
    reason: Any
    def __init__(self, resp, content, uri: Any | None = ...) -> None: ...
    @property
    def status_code(self): ...

class InvalidJsonError(Error): ...
class UnknownFileType(Error): ...
class UnknownLinkType(Error): ...
class UnknownApiNameOrVersion(Error): ...
class UnacceptableMimeTypeError(Error): ...
class MediaUploadSizeError(Error): ...
class ResumableUploadError(HttpError): ...
class InvalidChunkSizeError(Error): ...
class InvalidNotificationError(Error): ...

class BatchError(HttpError):
    resp: Any
    content: Any
    reason: Any
    def __init__(
        self, reason, resp: Any | None = ..., content: Any | None = ...
    ) -> None: ...

class UnexpectedMethodError(Error):
    def __init__(self, methodId: Any | None = ...) -> None: ...

class UnexpectedBodyError(Error):
    def __init__(self, expected, provided) -> None: ...

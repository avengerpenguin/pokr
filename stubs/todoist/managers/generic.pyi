from typing import Any

class Manager:
    state_name: Any
    object_type: Any
    api: Any
    def __init__(self, api) -> None: ...
    @property
    def state(self): ...
    @property
    def queue(self): ...
    @property
    def token(self): ...

class AllMixin:
    def all(self, filt: Any | None = ...): ...

class GetByIdMixin:
    def get_by_id(self, obj_id, only_local: bool = ...): ...

class SyncMixin:
    def sync(self): ...

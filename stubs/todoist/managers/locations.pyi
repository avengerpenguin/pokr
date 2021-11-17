from typing import Any

from .generic import AllMixin as AllMixin
from .generic import Manager as Manager
from .generic import SyncMixin as SyncMixin

class LocationsManager(Manager, AllMixin, SyncMixin):
    state_name: str
    object_type: Any
    def clear(self) -> None: ...

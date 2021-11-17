from typing import Any

from .generic import AllMixin as AllMixin
from .generic import GetByIdMixin as GetByIdMixin
from .generic import Manager as Manager
from .generic import SyncMixin as SyncMixin

class LiveNotificationsManager(Manager, GetByIdMixin, AllMixin, SyncMixin):
    state_name: str
    object_type: Any
    def set_last_read(self, id) -> None: ...
    def mark_read(self, id) -> None: ...
    def mark_read_all(self) -> None: ...
    def mark_unread(self, id) -> None: ...

from .. import models as models
from .generic import AllMixin as AllMixin
from .generic import GetByIdMixin as GetByIdMixin
from .generic import Manager as Manager
from .generic import SyncMixin as SyncMixin

class RemindersManager(Manager, AllMixin, GetByIdMixin, SyncMixin):
    state_name: str
    object_type: str
    def add(self, item_id, **kwargs): ...
    def update(self, reminder_id, **kwargs) -> None: ...
    def delete(self, reminder_id) -> None: ...
    def get(self, reminder_id): ...

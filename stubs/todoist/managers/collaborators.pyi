from typing import Any

from .generic import GetByIdMixin as GetByIdMixin
from .generic import Manager as Manager
from .generic import SyncMixin as SyncMixin

class CollaboratorsManager(Manager, GetByIdMixin, SyncMixin):
    state_name: str
    object_type: Any
    def delete(self, project_id, email) -> None: ...

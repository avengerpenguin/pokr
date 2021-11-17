from typing import Any

from .generic import Manager as Manager
from .generic import SyncMixin as SyncMixin

class CollaboratorStatesManager(Manager, SyncMixin):
    state_name: str
    object_type: Any
    def get_by_ids(self, project_id, user_id): ...

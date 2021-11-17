from typing import Any

from .generic import Manager as Manager
from .generic import SyncMixin as SyncMixin

class InvitationsManager(Manager, SyncMixin):
    state_name: Any
    object_type: str
    def accept(self, invitation_id, invitation_secret) -> None: ...
    def reject(self, invitation_id, invitation_secret) -> None: ...
    def delete(self, invitation_id) -> None: ...

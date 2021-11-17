from typing import Any

from .generic import Manager as Manager

class BizInvitationsManager(Manager):
    state_name: Any
    object_type: Any
    def accept(self, invitation_id, invitation_secret) -> None: ...
    def reject(self, invitation_id, invitation_secret) -> None: ...

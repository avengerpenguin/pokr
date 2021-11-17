from .. import models as models
from .generic import AllMixin as AllMixin
from .generic import GetByIdMixin as GetByIdMixin
from .generic import Manager as Manager
from .generic import SyncMixin as SyncMixin

class GenericNotesManager(Manager, AllMixin, GetByIdMixin, SyncMixin):
    object_type: str
    def update(self, note_id, **kwargs) -> None: ...
    def delete(self, note_id) -> None: ...

class NotesManager(GenericNotesManager):
    state_name: str
    def add(self, item_id, content, **kwargs): ...
    def get(self, note_id): ...

class ProjectNotesManager(GenericNotesManager):
    state_name: str
    def add(self, project_id, content, **kwargs): ...
    def get(self, note_id): ...

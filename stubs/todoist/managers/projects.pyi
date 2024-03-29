from .. import models as models
from .generic import AllMixin as AllMixin
from .generic import GetByIdMixin as GetByIdMixin
from .generic import Manager as Manager
from .generic import SyncMixin as SyncMixin

class ProjectsManager(Manager, AllMixin, GetByIdMixin, SyncMixin):
    state_name: str
    object_type: str
    def add(self, name, **kwargs): ...
    def update(self, project_id, **kwargs) -> None: ...
    def delete(self, project_id) -> None: ...
    def archive(self, project_id) -> None: ...
    def unarchive(self, project_id) -> None: ...
    def move(self, project_id, parent_id) -> None: ...
    def reorder(self, projects) -> None: ...
    def share(self, project_id, email) -> None: ...
    def get_archived(self): ...
    def get_data(self, project_id): ...
    def get(self, project_id): ...

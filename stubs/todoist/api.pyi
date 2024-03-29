from typing import Any

from todoist import models as models
from todoist.managers.activity import ActivityManager as ActivityManager
from todoist.managers.archive import (
    ItemsArchiveManagerMaker as ItemsArchiveManagerMaker,
)
from todoist.managers.archive import (
    SectionsArchiveManagerMaker as SectionsArchiveManagerMaker,
)
from todoist.managers.backups import BackupsManager as BackupsManager
from todoist.managers.biz_invitations import (
    BizInvitationsManager as BizInvitationsManager,
)
from todoist.managers.business_users import (
    BusinessUsersManager as BusinessUsersManager,
)
from todoist.managers.collaborator_states import (
    CollaboratorStatesManager as CollaboratorStatesManager,
)
from todoist.managers.collaborators import (
    CollaboratorsManager as CollaboratorsManager,
)
from todoist.managers.completed import CompletedManager as CompletedManager
from todoist.managers.emails import EmailsManager as EmailsManager
from todoist.managers.filters import FiltersManager as FiltersManager
from todoist.managers.invitations import (
    InvitationsManager as InvitationsManager,
)
from todoist.managers.items import ItemsManager as ItemsManager
from todoist.managers.labels import LabelsManager as LabelsManager
from todoist.managers.live_notifications import (
    LiveNotificationsManager as LiveNotificationsManager,
)
from todoist.managers.locations import LocationsManager as LocationsManager
from todoist.managers.notes import NotesManager as NotesManager
from todoist.managers.notes import ProjectNotesManager as ProjectNotesManager
from todoist.managers.projects import ProjectsManager as ProjectsManager
from todoist.managers.quick import QuickManager as QuickManager
from todoist.managers.reminders import RemindersManager as RemindersManager
from todoist.managers.sections import SectionsManager as SectionsManager
from todoist.managers.templates import TemplatesManager as TemplatesManager
from todoist.managers.uploads import UploadsManager as UploadsManager
from todoist.managers.user import UserManager as UserManager
from todoist.managers.user_settings import (
    UserSettingsManager as UserSettingsManager,
)

DEFAULT_API_VERSION: str

class SyncError(Exception): ...

class TodoistAPI:
    @classmethod
    def deserialize(cls, data): ...
    api_endpoint: Any
    api_version: Any
    token: Any
    temp_ids: Any
    queue: Any
    session: Any
    biz_invitations: Any
    collaborators: Any
    collaborator_states: Any
    filters: Any
    invitations: Any
    items: Any
    labels: Any
    live_notifications: Any
    locations: Any
    notes: Any
    projects: Any
    project_notes: Any
    reminders: Any
    sections: Any
    user: Any
    user_settings: Any
    activity: Any
    backups: Any
    business_users: Any
    completed: Any
    emails: Any
    quick: Any
    templates: Any
    uploads: Any
    items_archive: Any
    sections_archive: Any
    cache: Any
    def __init__(
        self,
        token: str = ...,
        api_endpoint: str = ...,
        api_version=...,
        session: Any | None = ...,
        cache: str = ...,
    ) -> None: ...
    sync_token: str
    state: Any
    def reset_state(self) -> None: ...
    def __getitem__(self, key): ...
    def serialize(self): ...
    def get_api_url(self): ...
    def generate_uuid(self): ...
    def sync(self, commands: Any | None = ...): ...
    def commit(self, raise_on_error: bool = ...): ...
    def query(self, queries, **kwargs): ...
    def add_item(self, content, **kwargs): ...

def state_default(obj): ...
def json_default(obj): ...

json_dumps: Any

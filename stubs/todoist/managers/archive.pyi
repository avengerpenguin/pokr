from typing import Any, Dict, Iterator, Optional

from ..api import TodoistAPI as TodoistAPI
from ..models import Item as Item
from ..models import Model as Model
from ..models import Section as Section

class ArchiveManager:
    object_model: Any
    api: Any
    element_type: Any
    def __init__(self, api: TodoistAPI, element_type: str) -> None: ...
    def next_page(self, cursor: Optional[str]) -> Dict: ...

class SectionsArchiveManagerMaker:
    api: Any
    def __init__(self, api) -> None: ...
    def for_project(self, project_id): ...

class SectionsArchiveManager(ArchiveManager):
    object_model: Any
    project_id: Any
    def __init__(self, api, project_id) -> None: ...
    def sections(self) -> Iterator[Section]: ...

class ItemsArchiveManagerMaker:
    api: Any
    def __init__(self, api) -> None: ...
    def for_project(self, project_id): ...
    def for_section(self, section_id): ...
    def for_parent(self, parent_id): ...

class ItemsArchiveManager(ArchiveManager):
    object_model: Any
    project_id: Any
    section_id: Any
    parent_id: Any
    def __init__(
        self,
        api,
        project_id: Any | None = ...,
        section_id: Any | None = ...,
        parent_id: Any | None = ...,
    ) -> None: ...
    def items(self) -> Iterator[Item]: ...

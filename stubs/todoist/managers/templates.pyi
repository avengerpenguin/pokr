from .generic import Manager as Manager

class TemplatesManager(Manager):
    def import_into_project(self, project_id, filename, **kwargs): ...
    def export_as_file(self, project_id, **kwargs): ...
    def export_as_url(self, project_id, **kwargs): ...

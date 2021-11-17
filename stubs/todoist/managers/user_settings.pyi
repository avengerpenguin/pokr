from .generic import Manager as Manager

class UserSettingsManager(Manager):
    def update(self, **kwargs) -> None: ...

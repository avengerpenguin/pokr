from typing import Any

from .generic import Manager as Manager

class UserManager(Manager):
    def update(self, **kwargs) -> None: ...
    def update_goals(self, **kwargs) -> None: ...
    def sync(self): ...
    def get(self, key: Any | None = ..., default: Any | None = ...): ...
    def get_id(self): ...
    def login(self, email, password): ...
    def login_with_google(self, email, oauth2_token, **kwargs): ...
    def register(self, email, full_name, password, **kwargs): ...
    def delete(self, current_password, **kwargs): ...
    def update_notification_setting(
        self, notification_type, service, dont_notify
    ): ...

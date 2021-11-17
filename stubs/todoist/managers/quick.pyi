from .generic import Manager as Manager

class QuickManager(Manager):
    def add(self, text, **kwargs): ...

import abc
from typing import Any

class Cache(metaclass=abc.ABCMeta):
    __metaclass__: Any
    @abc.abstractmethod
    def get(self, url): ...
    @abc.abstractmethod
    def set(self, url, content): ...

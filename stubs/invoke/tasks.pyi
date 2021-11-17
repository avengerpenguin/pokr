from typing import Callable, Dict

class Task:
    body: Callable
    name: str
    help: Dict

def task(*args, **kwargs): ...

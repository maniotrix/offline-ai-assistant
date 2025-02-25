from base.base_observer import Observable
from typing import TypeVar

T = TypeVar("T")
class BaseService(Observable[T]):
    pass

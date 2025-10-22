from typing import Any, Optional
from abc import ABC, abstractmethod

class DatabaseManager(ABC):

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def execute(self, query: str , params: tuple = ()) -> None:
        pass

    @abstractmethod
    def fetch_all(self, query: str, params: tuple = ()) -> list[Any]:
        pass

    @abstractmethod
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Any]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass



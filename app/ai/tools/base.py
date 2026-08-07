from abc import ABC
from abc import abstractmethod


class Tool(ABC):

    name: str

    @abstractmethod
    def execute(self) -> str:
        pass
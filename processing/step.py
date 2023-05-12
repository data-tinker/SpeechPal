from abc import ABC, abstractmethod


class AbstractStep(ABC):
    @abstractmethod
    def process(self):
        pass

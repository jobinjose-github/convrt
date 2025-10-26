from abc import ABC, abstractmethod


class Service(ABC):
    @abstractmethod
    def convert(self, file, source_type, target_type):
        pass
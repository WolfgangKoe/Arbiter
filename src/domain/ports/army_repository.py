from abc import ABC, abstractmethod

from src.domain.models.army import Army


class ArmyRepository(ABC):
    @abstractmethod
    def get_army(self) -> Army: ...

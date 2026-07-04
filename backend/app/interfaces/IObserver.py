from abc import ABC, abstractmethod


class IObserver(ABC):
    @abstractmethod
    def update(self, event_type: str, data: dict):
        pass


class ISubject(ABC):
    @abstractmethod
    def attach(self, observer: IObserver):
        pass

    @abstractmethod
    def detach(self, observer: IObserver):
        pass

    @abstractmethod
    def notify(self, event_type: str, data: dict):
        pass

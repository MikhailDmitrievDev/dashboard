from abc import ABC, abstractmethod


class IRepository(ABC):

    @abstractmethod
    def get(self):
        raise NotImplementedError

    def create(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

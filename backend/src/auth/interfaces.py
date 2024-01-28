from abc import ABC, abstractmethod


class IAuthService(ABC):
    @abstractmethod
    def sign_up(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def sign_in(self, *args, **kwargs):
        raise NotImplementedError

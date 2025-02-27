from abc import ABC, abstractmethod

from fastapi import APIRouter


class BaseController(ABC):
    prefix = None

    def configure_router(self) -> APIRouter:
        router = APIRouter(prefix=self.prefix)
        return self._configure_router(router)

    @abstractmethod
    def _configure_router(self, router: APIRouter) -> APIRouter:
        raise NotImplementedError

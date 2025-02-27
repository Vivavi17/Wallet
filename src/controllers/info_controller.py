from http import HTTPMethod

from fastapi import APIRouter

from controllers.base import BaseController


class InfoController(BaseController):
    prefix = ""

    def _configure_router(self, router: APIRouter) -> APIRouter:
        router.add_api_route("/ping", self.ping, methods=[HTTPMethod.GET])
        return router

    async def ping(self) -> int:
        return 200

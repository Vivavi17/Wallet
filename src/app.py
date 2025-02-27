from typing import Sequence

from fastapi import FastAPI, Request

from controllers.base import BaseController
from entities.exceptions import NotEnoughFundsException
from exceptions import (NotEnoughFundsHTTPException,
                        WalletDoesntExistHTTPException)
from service.exceptions import WalletDoesntExistServiceException


class Application(FastAPI):
    root_path = "/api/v1"

    def __init__(self, controllers: Sequence[BaseController]):
        self._controllers = controllers
        super().__init__(root_path=self.root_path)

    def configure_app(self):
        for controller in self._controllers:
            self.include_router(controller.configure_router())
        self.exception_handler(NotEnoughFundsException)(self.not_enough_funds)
        self.exception_handler(WalletDoesntExistServiceException)(
            self.wallet_doesnt_exist
        )
        return self

    def not_enough_funds(self, req: Request, exc: NotEnoughFundsException):
        raise NotEnoughFundsHTTPException

    def wallet_doesnt_exist(self, req: Request, exc: WalletDoesntExistServiceException):
        raise WalletDoesntExistHTTPException

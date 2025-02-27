from http import HTTPMethod
from uuid import UUID

from fastapi import APIRouter

from controllers.base import BaseController
from controllers.wallet_model import OperationEnum, WalletOperationModel
from entities.wallet import Wallet, WalletBalance
from service.service import AbstractService


class WalletController(BaseController):
    prefix = "/wallets"

    def __init__(self, service: AbstractService):
        self._service = service

    def _configure_router(self, router: APIRouter) -> APIRouter:
        router.add_api_route("/wallet", self.create_wallet, methods=[HTTPMethod.POST])
        router.add_api_route(
            "/{wallet_uuid}/operation",
            self.balance_operation,
            methods=[HTTPMethod.POST],
        )
        router.add_api_route(
            "/{wallet_uuid}", self.get_balance, methods=[HTTPMethod.GET]
        )
        return router

    async def create_wallet(self) -> Wallet:
        return await self._service.create()

    async def balance_operation(
        self, wallet_uuid: UUID, operation: WalletOperationModel
    ) -> None:
        if operation.operationType == OperationEnum.DEPOSIT:
            await self._service.deposit(wallet_uuid, operation.amount)
        elif operation.operationType == OperationEnum.WITHDRAW:
            await self._service.withdraw(wallet_uuid, operation.amount)

    async def get_balance(self, wallet_uuid: UUID) -> WalletBalance:
        return await self._service.get_balance(wallet_uuid)

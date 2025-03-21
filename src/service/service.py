from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Type
from uuid import UUID

from entities.wallet import Wallet, WalletBalance
from infra.uow import UnitOfWorkFactory
from infra.wallet_repository import WalletRepository
from service.exceptions import WalletDoesntExistServiceException


class AbstractService(ABC):
    def __init__(
        self, wallet_repository: Type[WalletRepository], uow_factory: UnitOfWorkFactory
    ):
        self.wallet_repository = wallet_repository
        self.uow_factory = uow_factory

    @abstractmethod
    async def create(self) -> Wallet:
        raise NotImplementedError

    @abstractmethod
    async def deposit(self, wallet_id: UUID, amount: Decimal):
        raise NotImplementedError

    @abstractmethod
    async def withdraw(self, wallet_id: UUID, amount: Decimal):
        raise NotImplementedError

    @abstractmethod
    async def get_balance(self, wallet_id: UUID) -> WalletBalance:
        raise NotImplementedError


class WalletService(AbstractService):
    async def create(self) -> Wallet:
        async with self.uow_factory() as uow:
            wallet = await uow.get(self.wallet_repository).create(Wallet())
        return wallet

    async def deposit(self, wallet_id: UUID, amount: Decimal) -> None:
        async with self.uow_factory() as uow:
            wallet = await self._get_wallet(uow, wallet_id)
            wallet.deposit(amount)
            await uow.get(self.wallet_repository).save(wallet)

    async def withdraw(self, wallet_id: UUID, amount: Decimal) -> None:
        async with self.uow_factory() as uow:
            wallet = await self._get_wallet(uow, wallet_id)
            wallet.withdraw(amount)
            await uow.get(self.wallet_repository).save(wallet)

    async def get_balance(self, wallet_id: UUID) -> WalletBalance:
        async with self.uow_factory() as uow:
            wallet = await uow.get(
                self.wallet_repository
            ).get_by_id_without_transaction(wallet_id)
            if not wallet:
                raise WalletDoesntExistServiceException
        return wallet.balance

    async def _get_wallet(self, uow, wallet_id: UUID) -> Wallet:
        wallet = await uow.get(self.wallet_repository).get_by_id(wallet_id)
        if not wallet:
            raise WalletDoesntExistServiceException
        return wallet

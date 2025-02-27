from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID

from entities.wallet import Wallet, WalletBalance
from infra.wallet_repository import AbstractRepository
from service.exceptions import WalletDoesntExistServiceException


class AbstractService(ABC):
    def __init__(self, repository: AbstractRepository):
        self._repository = repository

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
        wallet = await self._repository.create()
        return wallet

    async def deposit(self, wallet_id: UUID, amount: Decimal) -> None:
        async with self._repository.transaction() as session:
            wallet = await self._get_wallet(session, wallet_id)
            wallet.deposit(amount)
            await self._repository.save(session, wallet)

    async def withdraw(self, wallet_id: UUID, amount: Decimal) -> None:
        async with self._repository.transaction() as session:
            wallet = await self._get_wallet(session, wallet_id)
            wallet.withdraw(amount)
            await self._repository.save(session, wallet)

    async def get_balance(self, wallet_id: UUID) -> WalletBalance:
        wallet = await self._repository.get_by_id_without_transaction(wallet_id)
        if not wallet:
            raise WalletDoesntExistServiceException
        return wallet.balance

    async def _get_wallet(self, session, wallet_id: UUID) -> Wallet:
        wallet = await self._repository.get_by_id(session, wallet_id)
        if not wallet:
            raise WalletDoesntExistServiceException
        return wallet

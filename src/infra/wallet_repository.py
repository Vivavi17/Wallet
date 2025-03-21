from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from entities.wallet import Wallet, WalletBalance
from infra.database import WalletModel


class AbstractRepository(ABC):
    def __init__(self, session: AsyncSession):
        self._session = session

    @abstractmethod
    async def create(self, wallet: Wallet) -> Wallet:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, wallet_id: UUID) -> Wallet | None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, wallet: Wallet):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id_without_transaction(self, wallet_id: UUID) -> Wallet | None:
        raise NotImplementedError


class WalletRepository(AbstractRepository):

    async def get_by_id_without_transaction(self, wallet_id: UUID) -> Wallet | None:
        result = await self._session.execute(
            select(WalletModel).filter_by(id=wallet_id)
        )
        wallet = result.scalar_one_or_none()
        if wallet:
            wallet = Wallet(
                id=wallet.id, balance=WalletBalance(amount=Decimal(wallet.balance))
            )
        return wallet

    async def get_by_id(self, wallet_id: UUID) -> Wallet | None:
        result = await self._session.execute(
            select(WalletModel).filter_by(id=wallet_id).with_for_update()
        )
        wallet = result.scalar_one_or_none()
        if wallet:
            wallet = Wallet(
                id=wallet.id, balance=WalletBalance(amount=Decimal(wallet.balance))
            )
        return wallet

    async def save(self, wallet: Wallet) -> None:
        wallet = WalletModel(**wallet.dump())
        await self._session.execute(
            update(WalletModel).filter_by(id=wallet.id).values(balance=wallet.balance)
        )

    async def create(self, wallet: Wallet) -> Wallet:
        stmt = insert(WalletModel).values(wallet.dump()).returning("*")
        result = await self._session.execute(stmt)
        wallet_model = result.mappings().one()

        wallet = Wallet(
            id=wallet_model.id,
            balance=WalletBalance(amount=Decimal(wallet_model.balance)),
        )
        return wallet

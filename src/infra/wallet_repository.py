from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from entities.wallet import Wallet, WalletBalance
from infra.database import WalletModel


class AbstractRepository(ABC):
    @abstractmethod
    async def create(self) -> Wallet:
        raise NotImplementedError

    @abstractmethod
    async def transaction(self) -> AsyncSession:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, session: AsyncSession, wallet_id: UUID) -> Wallet | None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, session: AsyncSession, wallet: Wallet):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id_without_transaction(self, wallet_id: UUID) -> Wallet | None:
        raise NotImplementedError


class WalletRepository(AbstractRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory

    @asynccontextmanager
    async def transaction(self) -> AsyncSession:
        async with self._session_factory() as session:
            async with session.begin():
                try:
                    yield session
                except Exception:
                    await session.rollback()
                    raise
                else:
                    await session.commit()

    async def get_by_id_without_transaction(self, wallet_id: UUID) -> Wallet | None:
        async with self._session_factory() as session:
            result = await session.execute(select(WalletModel).filter_by(id=wallet_id))
            wallet = result.scalar_one_or_none()
            if wallet:
                wallet = Wallet(
                    id=wallet.id, balance=WalletBalance(amount=Decimal(wallet.balance))
                )
        return wallet

    async def get_by_id(self, session: AsyncSession, wallet_id: UUID) -> Wallet | None:
        result = await session.execute(
            select(WalletModel).filter_by(id=wallet_id).with_for_update()
        )
        wallet = result.scalar_one_or_none()
        if wallet:
            wallet = Wallet(
                id=wallet.id, balance=WalletBalance(amount=Decimal(wallet.balance))
            )
        return wallet

    async def save(self, session: AsyncSession, wallet: Wallet) -> None:
        wallet = WalletModel(**wallet.dump())
        await session.execute(
            update(WalletModel).filter_by(id=wallet.id).values(balance=wallet.balance)
        )

    async def create(self) -> Wallet:
        async with self._session_factory() as session:
            wallet_model = WalletModel()
            session.add(wallet_model)
            await session.commit()
            wallet = Wallet(
                id=wallet_model.id,
                balance=WalletBalance(amount=Decimal(wallet_model.balance)),
            )
            return wallet

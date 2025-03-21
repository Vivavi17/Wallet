from collections.abc import Callable
from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from infra.wallet_repository import AbstractRepository


class UnitOfWorkFactory:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory

    @asynccontextmanager
    async def __call__(self):
        async with self._session_factory() as session:
            async with session.begin():
                try:
                    yield UnitOfWork(session=session)
                except Exception:
                    await session.rollback()
                    raise
                else:
                    await session.commit()


class UnitOfWork:
    def __init__(self, session):
        self._session = session

    @lru_cache
    def get(self, repository: Type[AbstractRepository]):
        return repository(self._session)

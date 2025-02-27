import random
from contextlib import asynccontextmanager
from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app import Application
from controllers.wallets_controller import WalletController
from entities.wallet import Wallet, WalletBalance
from infra.wallet_repository import AbstractRepository
from service.service import AbstractService, WalletService


class TestRepository(AbstractRepository):
    wallets = {}

    @asynccontextmanager
    async def transaction(self):
        yield

    async def get_by_id(self, session, wallet_id: UUID) -> Wallet:
        return self.wallets.get(wallet_id)

    async def save(self, session, wallet: Wallet):
        self.wallets[wallet.id] = wallet

    async def create(self):
        wallet = Wallet()
        self.wallets[wallet.id] = wallet
        return wallet

    async def get_by_id_without_trans(self, wallet_id: UUID) -> Wallet | None:
        return self.wallets.get(wallet_id)


@pytest.fixture()
def t_wallet() -> Wallet:
    return Wallet(
        id="7759baaa-71cc-45b8-9b84-3e49795194ed", balance=WalletBalance(Decimal(100))
    )


@pytest.fixture(scope="module")
def t_repository() -> AbstractRepository:
    repository = TestRepository()
    return repository


@pytest.fixture(scope="module")
def wallets_id(t_repository) -> list[UUID]:
    for i in range(3):
        uuid = uuid4()
        t_repository.wallets[uuid] = Wallet(
            id=uuid, balance=WalletBalance(Decimal(random.randint(50, 100)))
        )
    return list(t_repository.wallets.keys())


@pytest.fixture(scope="module")
def t_service(t_repository) -> AbstractService:
    return WalletService(t_repository)


@pytest.fixture()
def test_client(t_service) -> TestClient:
    controller = WalletController(t_service)
    app = Application([controller])
    app = app.configure_app()
    return TestClient(app)

from contextlib import nullcontext as does_not_raise
from decimal import Decimal

import pytest

from entities.exceptions import NotEnoughFundsException


@pytest.mark.parametrize(
    "amount",
    [
        Decimal(10),
        Decimal(50),
        Decimal(0.5),
    ],
)
async def test_deposit(amount, wallets_id, t_service):
    for wallet_id in wallets_id:
        curr_balance = await t_service.get_balance(wallet_id)
        await t_service.deposit(wallet_id, amount)
        new_balance = await t_service.get_balance(wallet_id)
        assert new_balance.amount == curr_balance.amount + amount


@pytest.mark.parametrize(
    "amount",
    [
        Decimal(10),
        Decimal(0.5),
    ],
)
async def test_withdraw(amount, wallets_id, t_service):
    for wallet_id in wallets_id:
        curr_balance = await t_service.get_balance(wallet_id)
        await t_service.withdraw(wallet_id, amount)
        new_balance = await t_service.get_balance(wallet_id)
        assert new_balance.amount == curr_balance.amount - amount


@pytest.mark.parametrize(
    "amount,expectation",
    [
        (Decimal(10), does_not_raise()),
        (Decimal(9999999), pytest.raises(NotEnoughFundsException)),
    ],
)
async def test_withdraw(amount, expectation, wallets_id, t_service):
    with expectation:
        for wallet_id in wallets_id:
            await t_service.withdraw(wallet_id, amount)

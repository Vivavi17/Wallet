from contextlib import nullcontext as does_not_raise
from decimal import Decimal

import pytest
from pydantic_core import ValidationError

from entities.exceptions import NotEnoughFundsException
from entities.wallet import Wallet, WalletBalance


@pytest.mark.parametrize(
    "balance,expectation",
    [(1, does_not_raise()), (-1, pytest.raises(NotEnoughFundsException))],
)
def test_balance_exc(balance, expectation):
    with expectation:
        assert WalletBalance(Decimal(balance))


@pytest.mark.parametrize(
    "w_id,balance,expectation",
    [
        ("notuuid", WalletBalance(Decimal(0)), pytest.raises(ValidationError)),
        (
            "7759baaa-71cc-45b8-9b84-3e49795194ed",
            WalletBalance(Decimal(0)),
            does_not_raise(),
        ),
    ],
)
def test_wallet_exc(w_id, balance, expectation):
    with expectation:
        Wallet(id=w_id, balance=balance)


@pytest.mark.parametrize(
    "amount,result,", [(Decimal(100), Decimal(200)), (Decimal(0.5), Decimal(100.5))]
)
def test_deposit(amount, result, t_wallet):
    t_wallet.deposit(amount)
    assert result == t_wallet.balance.amount


@pytest.mark.parametrize(
    "amount,result", [(Decimal(1), Decimal(99)), (Decimal(9.5), Decimal(90.5))]
)
def test_withdraw(amount, result, t_wallet):
    t_wallet.withdraw(amount)
    assert result == t_wallet.balance.amount

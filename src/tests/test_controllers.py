from decimal import Decimal
from uuid import uuid4

import pytest


def test_get_balance_exist_wallet(wallets_id, test_client):
    response = test_client.get(f"api/v1/wallets/{wallets_id[0]}")
    assert response.status_code == 200


def test_get_balance_doesnt_exist_wallet(wallets_id, test_client):
    new_uuid = uuid4()
    response = test_client.get(f"api/v1/wallets/{new_uuid}")
    assert response.status_code == 404


def test_get_balance_incorrect_wallet(test_client):
    response = test_client.get(f"api/v1/wallets/notuuid")
    assert response.status_code == 422


def test_create_wallet(test_client):
    response = test_client.post("/api/v1/wallets/wallet")
    assert response.status_code == 200
    result = response.json()
    assert result.get("id") is not None
    assert result.get("balance") is not None
    assert result.get("balance").get("amount") == "0"


@pytest.mark.parametrize(
    "data,status_code",
    [
        ({"operationType": "DEPOSIT", "amount": 10}, 200),
        ({"operationType": "DEPOSIT", "amount": -10}, 422),
        ({"operationType": "deposit", "amount": 10}, 422),
        ({"operationType": "DEPOSIT"}, 422),
    ],
)
def test_wallet_deposit(data, status_code, wallets_id, test_client):
    curr_balance = test_client.get(f"api/v1/wallets/{wallets_id[0]}").json()
    response = test_client.post(f"/api/v1/wallets/{wallets_id[0]}/operation", json=data)
    assert response.status_code == status_code
    if status_code == 200:
        balance = test_client.get(f"api/v1/wallets/{wallets_id[0]}").json()
        assert Decimal(curr_balance["amount"]) + Decimal(data["amount"]) == Decimal(
            balance["amount"]
        )


@pytest.mark.parametrize(
    "data,status_code",
    [
        ({"operationType": "WITHDRAW", "amount": 10}, 200),
        ({"operationType": "WITHDRAW", "amount": -10}, 422),
        ({"operationType": "WITHDRAW", "amount": 999999}, 400),
        ({"operationType": "WITHDRAW"}, 422),
    ],
)
def test_wallet_withdraw(data, status_code, wallets_id, test_client):
    curr_balance = test_client.get(f"api/v1/wallets/{wallets_id[0]}").json()
    response = test_client.post(f"/api/v1/wallets/{wallets_id[0]}/operation", json=data)
    assert response.status_code == status_code
    if status_code == 200:
        balance = test_client.get(f"api/v1/wallets/{wallets_id[0]}").json()
        assert Decimal(curr_balance["amount"]) - Decimal(data["amount"]) == Decimal(
            balance["amount"]
        )

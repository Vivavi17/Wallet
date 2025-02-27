from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from entities.exceptions import NotEnoughFundsException


class ValueObject: ...


@dataclass(frozen=True)
class WalletBalance(ValueObject):
    amount: Decimal

    def __post_init__(self):
        if self.amount < 0:
            raise NotEnoughFundsException


class Wallet(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    balance: WalletBalance = Field(default=WalletBalance(Decimal(0)))

    def deposit(self, amount: Decimal) -> None:
        current_balance = self.balance.amount
        self.balance = WalletBalance(current_balance + amount)

    def withdraw(self, amount: Decimal) -> None:
        current_balance = self.balance.amount
        self.balance = WalletBalance(current_balance - amount)

    def dump(self) -> dict:
        return {"id": self.id, "balance": self.balance.amount}

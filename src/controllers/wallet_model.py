from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, field_validator


class OperationEnum(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletOperationModel(BaseModel):
    operationType: OperationEnum
    amount: Decimal

    @field_validator("amount")
    @classmethod
    def validate(cls, amount: Decimal) -> Decimal:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return amount

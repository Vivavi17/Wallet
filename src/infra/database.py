from uuid import uuid4

from sqlalchemy import DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __table_args__ = {"extend_existing": True}


class WalletModel(Base):
    __tablename__ = "wallet"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    balance: Mapped[float] = mapped_column(DECIMAL(18, 2), default=0.0, nullable=False)

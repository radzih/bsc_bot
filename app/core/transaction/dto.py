from dataclasses import dataclass
from datetime import datetime

from .model import TransactionStatus, TransactionType


@dataclass
class TransactionsList:
    user_id: int
    page: int
    per_page: int


@dataclass
class TransactionDTO:
    hash: str
    time: datetime
    amount_in_bnb: float
    amount_in_usd_now: float
    type: TransactionType
    status: TransactionStatus

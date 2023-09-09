from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    deposit = "deposit"
    withdraw = "withdraw"
    mint = "mint"
    approve = "approve"
    other = "other"


class TransactionStatus(Enum):
    success = "success"
    failed = "failed"


@dataclass
class Transaction:
    hash: str
    time: datetime
    amount_in_bnb: float
    amount_in_usd_now: float
    type: TransactionType
    status: TransactionStatus

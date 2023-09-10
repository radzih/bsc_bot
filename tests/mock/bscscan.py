from app.core.transaction.model import (
    Transaction,
    TransactionStatus,
    TransactionType,
)
from app.infra.bscscan.base import BASE_URL
from app.infra.bscscan.main import DEFAULT_OFFSET, BSCScanAdapter

BNB_PRICE = 500
LAST_BLOCK = 10000000
TRANSACTIONS = [
    Transaction(
        hash="0x1",
        time=1620000000,
        amount_in_bnb=0.1,
        amount_in_usd_now=100,
        type=TransactionType.deposit,
        status=TransactionStatus.success,
    )
]


class BSCScanMockAdapter(BSCScanAdapter):
    def __init__(self) -> None:
        self.bnb_price = BNB_PRICE
        self.last_block = LAST_BLOCK
        self.transactions = TRANSACTIONS

    async def get_bnb_price(self) -> float:
        return self.bnb_price

    async def get_last_block(self) -> int:
        return self.last_block

    async def get_transactions(
        self, address: str, page: int, offset: int = ...
    ) -> list[Transaction]:
        return self.transactions

    async def is_address_walid(self, address: str) -> bool:
        if address.startswith("0x"):
            return True
        return False

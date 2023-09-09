from typing import Any

from app.core.shared.interactor import Interactor
from app.infra.bscscan.main import BSCScanAdapter
from app.infra.db.main import DbGateway

from . import dto, exception


class ListTransactions(Interactor):
    def __init__(self, db: DbGateway, bscscan: BSCScanAdapter) -> None:
        self.db = db
        self.bscscan = bscscan

    async def __call__(self, data: dto.TransactionsList):
        user = await self.db.get_user(data.user_id)

        if not user or not user.wallet:
            raise exception.WalletNotSet(data.user_id)

        transactions = await self.bscscan.get_transactions(
            user.wallet, data.page, data.per_page
        )

        return [
            dto.TransactionDTO(
                hash=transaction.hash,
                time=transaction.time,
                amount_in_bnb=transaction.amount_in_bnb,
                amount_in_usd_now=transaction.amount_in_usd_now,
                type=transaction.type,
                status=transaction.status,
            )
            for transaction in transactions
        ]

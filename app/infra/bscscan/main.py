from asyncio import gather
from datetime import datetime
from time import time

from app.core.transaction.model import (
    Transaction,
    TransactionStatus,
    TransactionType,
)

from .base import BaseAdapter

FIRST_BLOCK = 0
FUNCTION_TRANSFER = "transfer"
DEFAULT_OFFSET = 10


class BSCScanAdapter(BaseAdapter):
    async def is_address_walid(self, address: str) -> bool:
        params = {
            "module": "account",
            "action": "balance",
            "address": address,
        }
        data = await self._get("", params=params)

        return data["status"] == "1"

    async def get_last_block(self) -> int:
        params = {
            "module": "block",
            "action": "getblocknobytime",
            "timestamp": int(time()),
            "closest": "before",
        }
        data = await self._get("", params=params)
        return int(data["result"])

    async def get_bnb_price(self) -> float:
        params = {
            "module": "stats",
            "action": "bnbprice",
        }
        data = await self._get("", params=params)
        return float(data["result"]["ethusd"])

    async def get_transactions(
        self, address: str, page: int, offset: int = DEFAULT_OFFSET
    ) -> list[Transaction]:
        last_block, bnb_price = await gather(
            self.get_last_block(), self.get_bnb_price()
        )
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": FIRST_BLOCK,
            "endblock": last_block,
            "offset": offset,
            "page": page,
            "sort": "desc",
        }

        data = await self._get("", params=params)

        result = []

        for tx in data["result"]:
            time = datetime.fromtimestamp(int(tx["timeStamp"]))
            hash_ = tx["hash"]
            amount_in_bnb = wei_to_bnb(int(tx["value"]))
            amount_in_usd_now = round(amount_in_bnb * bnb_price, 2)
            type_ = get_transaction_type(tx["functionName"], address, tx["to"])
            status = (
                TransactionStatus.success
                if int(tx["isError"]) == 0
                else TransactionStatus.failed
            )
            result.append(
                Transaction(
                    hash=hash_,
                    time=time,
                    amount_in_bnb=amount_in_bnb,
                    amount_in_usd_now=amount_in_usd_now,
                    type=type_,
                    status=status,
                )
            )
        return result


def wei_to_bnb(wei: int) -> float:
    return wei / 10**18


def get_transaction_type(
    function: str, user_address: str, transaction_to: str
) -> TransactionType:
    user_address = user_address.lower()
    transaction_to = transaction_to.lower()

    for type_ in TransactionType:
        if type_.value in function:
            return type_
        elif user_address == transaction_to and (
            FUNCTION_TRANSFER in function or function == ""
        ):
            return TransactionType.deposit
        elif user_address != transaction_to and (
            FUNCTION_TRANSFER in function or function == ""
        ):
            return TransactionType.withdraw
    return TransactionType.other

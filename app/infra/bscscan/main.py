from .base import BaseAdapter


class BSCScanAdapter(BaseAdapter):
    async def is_address_walid(self, address: str) -> bool:
        params = {
            "module": "account",
            "action": "balance",
            "address": address,
        }
        data = await self._get("", params=params)

        return data["status"] == "1"

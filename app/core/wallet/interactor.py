from app.core.shared.interactor import Interactor
from app.infra.bscscan.main import BSCScanAdapter


class IsValidWallet(Interactor):
    def __init__(self, bscscan_adapter: BSCScanAdapter) -> None:
        self.bscscan_adapter = bscscan_adapter

    async def __call__(self, data: str) -> bool:
        """
        Check if the wallet is valid.
        Return True if it is valid, False otherwise.
        """
        return await self.bscscan_adapter.is_address_walid(data)

from app.core.wallet.interactor import IsValidWallet


async def test_is_valid_wallet(is_valid_wallet: IsValidWallet) -> None:
    is_valid_valid = await is_valid_wallet("0x123")
    is_valid_invalid = await is_valid_wallet("invalid")

    assert is_valid_valid is True
    assert is_valid_invalid is False

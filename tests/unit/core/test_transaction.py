from pytest import raises

from app.core.transaction.dto import TransactionsList
from app.core.transaction.exception import WalletNotSet
from app.core.transaction.interactor import ListTransactions
from tests.mock.db import DbMockGateway


async def test_list_transactions_error(
    list_transactions: ListTransactions,
) -> None:
    with raises(WalletNotSet):
        await list_transactions(
            TransactionsList(user_id=1, page=1, per_page=10)
        )


async def test_list_transactions(
    list_transactions: ListTransactions, db_gateway: DbMockGateway
) -> None:
    await db_gateway.create_user(name="test", id=1)
    await db_gateway.commit()
    await db_gateway.update_user(user_id=1, wallet="0x123")
    await db_gateway.commit()

    transactions = await list_transactions(
        TransactionsList(user_id=1, page=1, per_page=1)
    )

    assert len(transactions) == 1

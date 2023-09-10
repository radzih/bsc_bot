from _pytest.scope import Scope
from pytest import fixture

from app.core.transaction.interactor import ListTransactions
from app.core.user.interactor import CreateUser, UpdateUser
from app.core.wallet.interactor import IsValidWallet
from tests.mock.bscscan import BSCScanMockAdapter
from tests.mock.db import DbMockGateway


@fixture(scope=Scope.Function)
def db_gateway() -> DbMockGateway:
    return DbMockGateway()


@fixture(scope=Scope.Function)
def bscscan_adapter() -> BSCScanMockAdapter:
    return BSCScanMockAdapter()


@fixture(scope=Scope.Function)
def create_user(db_gateway: DbMockGateway) -> CreateUser:
    return CreateUser(db_gateway)


@fixture(scope=Scope.Function)
def update_user(db_gateway: DbMockGateway) -> UpdateUser:
    return UpdateUser(db_gateway)


@fixture(scope=Scope.Function)
def is_valid_wallet(bscscan_adapter: BSCScanMockAdapter) -> IsValidWallet:
    return IsValidWallet(bscscan_adapter)


@fixture(scope=Scope.Function)
def list_transactions(
    bscscan_adapter: BSCScanMockAdapter, db_gateway: DbMockGateway
) -> ListTransactions:
    return ListTransactions(db_gateway, bscscan_adapter)

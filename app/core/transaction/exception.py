from dataclasses import dataclass

from app.core.shared.exception import AppException


@dataclass
class WalletNotSet(AppException):
    user_id: int

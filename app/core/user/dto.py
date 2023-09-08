from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserDTO:
    id: int
    name: str
    created_time: datetime
    wallet: str | None = None


@dataclass
class UserUpdate:
    id: int
    name: str | None = None
    wallet: str | None = None


@dataclass
class UserCreate:
    id: int
    name: str

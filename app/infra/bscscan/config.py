from dataclasses import dataclass
from os import environ


@dataclass
class BSCScan:
    api_key: str


def load_config() -> BSCScan:
    return BSCScan(
        api_key=environ["BSCSCAN_API_KEY"],
    )

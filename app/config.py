from dataclasses import dataclass
from logging import DEBUG, INFO, basicConfig
from os import environ

from app.infra.bscscan.config import BSCScan
from app.infra.bscscan.config import load_config as load_bscscan_config
from app.infra.db.config import Database
from app.infra.db.config import load_config as load_db_config
from app.present.bot.config import TgBot
from app.present.bot.config import load_config as load_bot_config


@dataclass
class Config:
    tg_bot: TgBot
    db: Database
    bscscan: BSCScan
    debug: bool = False


def load_config():
    return Config(
        tg_bot=load_bot_config(),
        db=load_db_config(),
        bscscan=load_bscscan_config(),
        debug=environ.get("DEBUG", False) == "True",
    )


def configure_logging(debug: bool) -> None:
    basicConfig(level=DEBUG if debug else INFO)

from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: int
    use_redis: bool
    tech_groups: int


@dataclass
class Miscellaneous:
    qiwi_token: str
    wallet: int
    qiwi_pay: str
    qiwi_sec: str
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=env.int("ADMINS"),
            use_redis=env.bool("USE_REDIS"),
            tech_groups=env.int("TECH_GROUPS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous(
            qiwi_token=env.str('QIWI'),
            wallet=env.int('WALLET'),
            qiwi_pay=env.str('QIWI_P_PAY'),
            qiwi_sec=env.str('QIWI_P_SICRET'),
        )
    )
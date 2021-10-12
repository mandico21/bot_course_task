import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from glQiwiApi import QiwiWrapper

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admins import setup_admins
from tgbot.handlers.inline import setup_inline
from tgbot.handlers.tools import setup_tools
from tgbot.handlers.users import setup_users
from tgbot.middlewares.db import DbMiddleware
from tgbot.misc.set_commands_bot import set_commands
from tgbot.services.database import create_db_session

logger = logging.getLogger(__name__)


def register_all_middlewares(dp):
    dp.setup_middleware(DbMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    setup_admins(dp)
    setup_tools(dp)
    setup_users(dp)
    setup_inline(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',

    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config
    bot['db'] = await create_db_session(config)
    bot['wallet'] = QiwiWrapper(api_access_token=config.misc.qiwi_token, phone_number=config.misc.wallet,
                                secret_p2p=config.misc.qiwi_sec)

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
        await set_commands(dp)
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")

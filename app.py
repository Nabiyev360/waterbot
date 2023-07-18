import asyncio

from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.rater import api_request



async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)

    db.create_table()



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(api_request())
    try:
        loop.run_until_complete(dp.start_polling())
    except KeyboardInterrupt:
        loop.run_until_complete(dp.stop_polling())
    finally:
        loop.close()

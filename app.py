import asyncio
import os

from aiogram import Bot,types, Dispatcher
from aiogram.enums import ParseMode
from dotenv import find_dotenv, load_dotenv
# Считываем токен из переменных окружения (.env)
load_dotenv(find_dotenv())

from handlers.user_private import user_private_router
from common.bot_cmds_list import private
from handlers.user_group import user_group_router

ALLOWED_UPDATES = ['message', 'edited_message']

bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
dp = Dispatcher()

dp.include_routers(user_private_router, user_group_router)


# Опрашиваем сервер телеграмм о наличии обновлений
async def main():
    # Не отвечает на сообщения, пока был оффлайн
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    # запрос
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())

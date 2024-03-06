import asyncio
import os

from aiogram import Bot,types, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.strategy import FSMStrategy

from dotenv import find_dotenv, load_dotenv
# Считываем токен из переменных окружения (.env)
load_dotenv(find_dotenv())

from middlewares.db import DataBaseSession

from database.engine import create_db, drop_db, session_maker

from handlers.user_private import user_private_router
from common.bot_cmds_list import private
from handlers.user_group import user_group_router
from handlers.admin_private import admin_router

# ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query']

bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
bot.my_admins_list = []
dp = Dispatcher()


dp.include_routers(user_private_router, user_group_router, admin_router)

async def on_startup(bot):
    run_param=False
    if run_param:
        await drop_db()
        
    await create_db()
    
async def on_shutdown(bot):
    print('бот лёг')
    

# Опрашиваем сервер телеграмм о наличии обновлений
async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    
    # Не отвечает на сообщения, пока был оффлайн
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    # запрос
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())

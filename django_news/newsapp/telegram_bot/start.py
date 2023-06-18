from aiogram import types, Dispatcher
from newsapp.telegram_bot.base import dp, bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo


#@dp.message_handler(commands=['start', 'help'])
async def command_start(msg:types.Message):
    help_msg = (f'Hello {msg.from_user.first_name}!\n'+
                f'Here are a few commands that can help you search and analyse news by different criteria:\n'
                f'/headlines - search news by keyword, country and category\n'+
                f'/everything - search news by keyword and language\n'+
                f'/registration - use this command to register\n(without it you can not see your collected articles)\n'+
                f'/articles - see your searched articles')
    help_msg_uk = (f'Привіт {msg.from_user.first_name}!\n'+
                    f'Ось декілька команд що допоможуть вам шукати та аналізовувати новини за різними критеріями:\n'
                    f'/headlines - шукати новини за країною, категорією та ключовим словом\n'+
                    f'/everything - шукати новини за мовою та ключовим словом\n'+
                    f'/registration - команда для реєстрації\n(без неї ти не сможеш зберігати свої, знайдені статті)\n'+
                    f'/articles - побачити збережені статті')
    if msg.from_user.language_code == 'uk' or 'ru' or 'bl':
        await bot.send_message(msg.from_user.id, help_msg_uk)
    else: await bot.send_message(msg.from_user.id, help_msg)


def heandlers_start(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    #dp.register_callback_query_handler(test_sesx, lambda c: c.data == '1' or c.data == '2')
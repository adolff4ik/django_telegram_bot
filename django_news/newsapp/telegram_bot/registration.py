from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from newsapp.telegram_bot.base import dp, bot
from aiogram import types, Dispatcher
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class FSMUser(StatesGroup):
    password = State()

@dp.message_handler(commands=['registration'])
async def password(msg: types.Message):
    await bot.send_message(msg.from_user.id,'Enter password')
    await FSMUser.password.set()

@dp.message_handler(state=FSMUser.password)
async def password2(msg: types.Message, state: FSMContext):
    user = await sync_to_async(User.objects.create_user)(username=msg.from_user.username,
                             first_name=msg.from_user.first_name,
                             password=msg.text
                             )
    await bot.send_message(msg.from_user.id,
                           f'Your user data:\nUsername:{msg.from_user.username}\n'+
                           f'First_name:{msg.from_user.first_name}\n'+
                           f'Password:||{msg.text}||',
                            parse_mode='MarkdownV2')
    await state.finish()

def heandlers_registration(dp : Dispatcher):
    dp.register_message_handler( password,commands=['registration'])
    dp.register_message_handler( password2,state=FSMUser.password)
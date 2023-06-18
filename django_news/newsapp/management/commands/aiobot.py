from aiogram.dispatcher.filters.state import State, StatesGroup
from newsapp.telegram_bot.base import dp
from newsapp.telegram_bot.start import heandlers_start
from newsapp.telegram_bot.news import heandlers_news
from django.core.management.base import BaseCommand


class FSMUser(StatesGroup):
    password = State()

heandlers_start(dp)
heandlers_news(dp)

def run_bot():
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        run_bot()
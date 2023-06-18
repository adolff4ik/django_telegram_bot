from django.contrib.auth.models import User
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from newsapp.utils.get_articles import get_articles
from newsapp.utils.results import results
from aiogram import types, Dispatcher
from asgiref.sync import sync_to_async
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot

storage = MemoryStorage()

bot = Bot('token')
dp = Dispatcher(bot, storage=storage)

class FSMHeadlines(StatesGroup):
    country = State()
    q = State()
    category = State()

class FSMEverything(StatesGroup):
    q = State()
    language = State()


FSMdict = {'FSMHeadlines':{'country':'Введіть ключове слово:','q':'Введіть категорію:','category':'Дякую за введені дані!',
                            'url':'https://newsapi.org/v2/top-headlines?apikey=', 'next':FSMHeadlines.next},
            'FSMEverything':{'q':'Введіть мову новин:','language':'Дякую за введені дані!',
                              'url':'https://newsapi.org/v2/everything?apikey=', 'next':FSMEverything.next}
            }

categories = ['business', 'general', 'technology',
              'entertainment','health',
              'sports', 'science', 'politics']
states = [FSMHeadlines.country,FSMHeadlines.q,FSMHeadlines.category,FSMEverything.q,FSMEverything.language]

keyboard = types.InlineKeyboardMarkup()
keyboard.add(types.InlineKeyboardButton("Пропустити", callback_data='skip'))

async def create_markup(i):
    markup = types.InlineKeyboardMarkup() #markup that lets you switch articles
    markup.row_width = 2
    markup.add(types.InlineKeyboardButton(text="<", callback_data=f"previous.{i}"),
    types.InlineKeyboardButton(text=">", callback_data=f"next.{i}"))
    return markup

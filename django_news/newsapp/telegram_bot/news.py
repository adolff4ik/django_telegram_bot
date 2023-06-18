from aiogram.dispatcher import FSMContext
from newsapp.telegram_bot.base import dp, bot
from .base import *
from newsapp.models import Article
from aiogram import types, Dispatcher
from asgiref.sync import sync_to_async


async def news_msg_send(msg_or_call,queryset_list):
    i = 0
    await bot.send_message(msg_or_call.from_user.id,
                            f"<a href='{queryset_list[i]}'>Дивитись статтю №{i+1}</a>",
                                parse_mode='html',
                                reply_markup=await create_markup(i))

async def news_msg(state,msg_or_call,post_data,fsm_status):
    try:
        user=await sync_to_async(User.objects.get)(username=msg_or_call.from_user.username)
    except:
        user=None
    articles_json = get_articles(api_url=FSMdict[fsm_status]['url'], params=post_data)
    queryset = await sync_to_async(results)(articles_json, post_data['q'], user=user)
    await state.finish()

    global queryset_list

    queryset_list = []
    for q in queryset:
        queryset_list.append(q['link'])
    
    await news_msg_send(msg_or_call,queryset_list)

async def msg_produssing(msg_or_call, state: FSMContext):
    stan = await state.get_state()
    param = stan.split(':')[1]
    print(param == 'q')
    if stan == 'FSMHeadlines:q':
        keyboard = types.ReplyKeyboardMarkup()
        for category in categories:
            keyboard.insert(types.KeyboardButton(category, one_time_keyboard=True))
        keyboard.add(types.KeyboardButton('skip', resize_keyboard=True))
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Пропустити", callback_data='skip'))
    try:
        value = msg_or_call.data
    except:
        value = msg_or_call.text

    if value == 'skip':
        value = ''
    async with state.proxy() as data:
        data[param] = value
        print(data)#
        post_data = data.as_dict()
    
    fsm_status = stan.split(':')[0]
    
    fsm_next = FSMdict[fsm_status]['next']
    
    if bool(await fsm_next()):
        await bot.send_message(msg_or_call.from_user.id, FSMdict[fsm_status][param], reply_markup=keyboard)
    else:
        await bot.send_message(msg_or_call.from_user.id, FSMdict[fsm_status][param], reply_markup=types.ReplyKeyboardRemove())
        await news_msg(state,msg_or_call,post_data,fsm_status)


#@dp.message_handler(commands=['headlines'])
async def start_headlines(msg: types.Message):
    await FSMHeadlines.country.set()
    await msg.reply('Введіть країну:', reply_markup=keyboard)

async def start_everything(msg: types.Message):
    await FSMEverything.q.set()
    await msg.reply('Введіть ключове слово:', reply_markup=keyboard)

#@dp.message_handler(commands=['articles'])
async def articles(msg: types.Message):
    try:
        user=await sync_to_async(User.objects.get)(username=msg.from_user.username)
    except:
        user=None
    articles = await sync_to_async(Article.objects.filter)(user=user)

    global queryset_list

    queryset_list = []
    async for article in articles:
        await sync_to_async(queryset_list.append)(article.link)
    
    await news_msg_send(msg,queryset_list)


#@dp.message_handler(state="*")
async def catch_state(msg: types.Message, state: FSMContext):
    await msg_produssing(msg, state)

#@dp.callback_query_handler(lambda c: c.data == 'skip', state="*")
async def skip(call: types.CallbackQuery, state: FSMContext):
    await msg_produssing(call, state)


#@dp.callback_query_handler(lambda c: c.data.startswith('next') or c.data.startswith('previous'))
async def switcher(call: types.CallbackQuery):
    param = call.data.split('.')[0]
    i = int(call.data.split('.')[1])

    if param == 'next':
        i += 1
    elif param == 'previous':
        i -= 1
    else:
        print('blyat`')

    await bot.edit_message_text(text=f"<a href='{queryset_list[i]}'>Дивитись статтю №{i+1}</a>",
    chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=await create_markup(i), parse_mode='html',)


def heandlers_news(dp : Dispatcher):
    dp.register_message_handler( articles,commands=['articles'])
    dp.register_message_handler( start_everything,commands=['everything'])
    dp.register_message_handler( start_headlines,commands=['headlines'])
    dp.register_message_handler( catch_state,state=states)
    dp.register_callback_query_handler( skip,lambda c: c.data == 'skip', state=states)
    dp.register_callback_query_handler( switcher,lambda c: c.data.startswith('next') or c.data.startswith('previous'))
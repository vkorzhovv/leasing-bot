import asyncio
from aiogram import types, executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardRemove
from services import *
from aiogram.dispatcher.filters import Command, Text
import re
from bot import storage, bot, dp, TOKEN, admin_id, domen
import logging
import datetime
from aiogram.types import InputMediaPhoto, InputFile


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='bot.log')


class BotStatesGroup(StatesGroup):

    name = State()
    location = State()
    company_name = State()
    phone = State()


class SearchStatesGroup(StatesGroup):
    category = State()
    wow = State()
    species = State()
    wheels = State()
    brand = State()
    country = State()
    year = State()

class ProductState(StatesGroup):
    # Состояние для отслеживания текущего элемента списка продуктов
    current_index = State()

class ItemState(StatesGroup):
    # Состояние для отслеживания текущего элемента списка продуктов
    current_index = State()

class PromotionState(StatesGroup):
    # Состояние для отслеживания текущего элемента списка продуктов
    current_index = State()


def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(KeyboardButton('/start'))

    return kb


def species(lst):
    keyboard = InlineKeyboardMarkup()
    l = set([i['species'] for i in lst])
    for d in l:
        if str(d)=='None':
            button = InlineKeyboardButton(f'Пропустить', callback_data=f'{d}')
        else:
            button = InlineKeyboardButton(f'{d}', callback_data=f'{d}')
        keyboard.row(button)
    return keyboard

def filters(lst):
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(f'фильтры', callback_data=f'123')
    keyboard.row(button)
    return keyboard

def brand(lst):
    keyboard = InlineKeyboardMarkup()
    l = set([i['brand'] for i in lst])
    for d in l:
        if str(d)=='None':
            button = InlineKeyboardButton(f'Пропустить', callback_data=f'{d}')
        else:
            button = InlineKeyboardButton(f'{d}', callback_data=f'{d}')
        keyboard.row(button)
    return keyboard


def country(lst):
    keyboard = InlineKeyboardMarkup()
    l = set([i['manufacturer'] for i in lst])
    for d in l:
        if str(d)=='None':
            button = InlineKeyboardButton(f'Пропустить', callback_data=f'{d}')
        else:
            button = InlineKeyboardButton(f'{d}', callback_data=f'{d}')
        keyboard.row(button)
    return keyboard

def year(lst):
    keyboard = InlineKeyboardMarkup()
    l = set([i['year'] for i in lst])
    for d in l:
        if str(d)=='None':
            button = InlineKeyboardButton(f'Пропустить', callback_data=f'{d}')
        else:
            button = InlineKeyboardButton(f'{d}', callback_data=f'{d}')
        keyboard.row(button)
    return keyboard

def wheels(lst):
    keyboard = InlineKeyboardMarkup()
    l = set([i['wheels'] for i in lst])
    for d in l:
        if str(d)=='None':
            button = InlineKeyboardButton(f'Пропустить', callback_data=f'{d}')
        else:
            button = InlineKeyboardButton(f'{d}', callback_data=f'{d}')
        keyboard.row(button)
    return keyboard

def search_kb():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(f'Категории', callback_data=f'Каталог')
    keyboard.row(button)
    return keyboard


def get_product_kb(media, products, kp):
    keyboard = InlineKeyboardMarkup()
    mediabutton = InlineKeyboardButton('Показать ещё', callback_data="media")
    button1 = InlineKeyboardButton('⬅️', callback_data="previous")
    button2 = InlineKeyboardButton('➡️', callback_data="next")
    button3 = InlineKeyboardButton('Чат с менеджером', callback_data="manager_chat")
    button4 = InlineKeyboardButton('Запрос на КП', callback_data="kp")
    button5 = InlineKeyboardButton('Меню 🚚', callback_data="models")
    if len(media)>0:
        keyboard.row(mediabutton)
    if len(products)>1:
        keyboard.row(button1, button2)
    if kp!=None:
        keyboard.row(button4)
    keyboard.row(button3)
    keyboard.row(button5)
    return keyboard

def get_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Меню 🚚', callback_data="models")
    keyboard.row(button)
    return keyboard

def get_location_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton("Поделиться геопозицией", request_location=True)
    button2 = types.KeyboardButton("Отказаться")
    keyboard.add(button)
    keyboard.add(button2)
    return keyboard

def get_items_kb(items):
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('⬅️', callback_data="previous_item")
    button2 = InlineKeyboardButton('➡️', callback_data="next_item")
    button3 = InlineKeyboardButton('Меню 🚚', callback_data="models")
    if len(items)>1:
        keyboard.row(button1, button2)
    keyboard.row(button3)
    return keyboard

def get_promotions_kb(media, promotions, kp):
    keyboard = InlineKeyboardMarkup()
    mediabutton = InlineKeyboardButton('Показать ещё', callback_data="media")
    button1 = InlineKeyboardButton('⬅️', callback_data="previous_promotion")
    button2 = InlineKeyboardButton('➡️', callback_data="next_promotion")
    button3 = InlineKeyboardButton('Чат с менеджером', callback_data="manager_chat")
    button4 = InlineKeyboardButton('Запрос на КП', callback_data="kp")
    button5 = InlineKeyboardButton('Меню 🚚', callback_data="models")
    if len(media)>0:
        keyboard.row(mediabutton)
    if len(promotions)>1:
        keyboard.row(button1, button2)
    if kp!=None:
        keyboard.row(button4)
    keyboard.row(button3)
    keyboard.row(button5)
    return keyboard

def activate_user_kb():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Подтвердить', callback_data="yes")
    button2 = InlineKeyboardButton('Отклонить', callback_data="no")
    keyboard.row(button1, button2)
    return keyboard

def get_categories_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Поиск'))
    kb.add(KeyboardButton('Каталог'), KeyboardButton('Акции'))
    kb.add(KeyboardButton('Новости'), KeyboardButton('Актуальное'))
    kb.add(KeyboardButton('О нас'))
    return kb


# Функция для создания inline клавиатуры с категориями
def create_category_keyboard(categories):
    keyboard = InlineKeyboardMarkup()
    for category in categories:
        button = InlineKeyboardButton(category['name'], callback_data=f"{category['id']}")
        keyboard.row(button)
    return keyboard

# Функция для создания inline клавиатуры с категориями
def create_category_keyboard_with_menu(categories):
    keyboard = InlineKeyboardMarkup()
    for category in categories:
        button = InlineKeyboardButton(category['name'], callback_data=f"{category['id']}")
        keyboard.row(button)
    keyboard.row(InlineKeyboardButton('Меню 🚚', callback_data="menu"))
    return keyboard


def get_phone_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(
        'Отправить мой сотовый номер боту ☎️', request_contact=True))
    kb.add(KeyboardButton('/cancel'))

    return kb


def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/cancel'))

    return kb


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return

    await state.finish()
    await message.reply('Вы прервали регистрацию!',
                        reply_markup=get_kb())


@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message) -> None:
    logging.info(f"Телеграм-пользователь {message.from_user.username} начал регистрацию")

    MESSAGES = await get_commands_list()

    if await check_botuser_exists(str(message.from_user.id)):
        MESSAGES = await get_commands_list()
        logging.info(f"Телеграм-пользователь {message.from_user.username} уже имеет зарегистрированный аккаунт")
        if 'already_registered_message' in MESSAGES:
            await bot.send_message(message.from_user.id, MESSAGES['already_registered_message'][0][3:-4].replace('<br />', ''))
        else:
            await create_command(key='already_registered_message', text='Вы уже зарегистрированы!'.replace('<br />', ''))
            MESSAGES = await get_commands_list()
            await bot.send_message(message.from_user.id, MESSAGES['already_registered_message'][0][3:-4])
    else:
        # await create_profile(user_id=message.from_user.id)
        if 'welcome_message' in MESSAGES:
            await send_photo_with_url(TOKEN=TOKEN, CHAT_ID=str(message.from_user.id), img_url=MESSAGES['welcome_message'][1], caption=MESSAGES['welcome_message'][0].replace('<br />', ''), parse_mode=types.ParseMode.HTML, message=message)
        else:
            await create_command(key='welcome_message', text='Приветствие. Авторизуйтесь. Введите ФИО')
            MESSAGES = await get_commands_list()
            await send_photo_with_url(TOKEN=TOKEN, CHAT_ID=str(message.from_user.id), img_url=MESSAGES['welcome_message'][1], caption=MESSAGES['welcome_message'][0].replace('<br />', ''), parse_mode=types.ParseMode.HTML, message=message)
        await BotStatesGroup.name.set()

@dp.message_handler(commands=['city'])
async def command_city(message: types.Message):
    command, city_name = message.get_full_command()
    bot_user = message.from_user.id

    if not city_name:
        await message.reply("Пожалуйста, укажите название города после команды /city.")
        return

    await update_botuser_city(user_id=str(bot_user), new_city=city_name)

    # Здесь вы можете выполнить какую-либо обработку для указанного города (например, запросы к API для получения информации)
    # Вместо этого примера, просто отправим сообщение с указанным городом
    await message.reply(f"Вы установили город: {city_name}")


@dp.message_handler(commands=['menu'], state='*')
async def cmd_menu(message: types.Message) -> None:
    logging.info(f"Телеграм-пользователь {message.from_user.username} нажал на меню")
    if await check_botuser_activated(str(message.from_user.id)):
        await bot.send_message(message.from_user.id, "Выберите пункт:", reply_markup = get_categories_kb())
    else:
        MESSAGES = await get_commands_list()
        if 'already_registered_message' in MESSAGES:
            await bot.send_message(message.from_user.id, MESSAGES['wait_for_approve_message'][0][3:-4].replace('<br />', ''))
        else:
            await create_command(key='wait_for_approve_message', text='Пользователь не подтверждён')
            MESSAGES = await get_commands_list()
            await bot.send_message(message.from_user.id, MESSAGES['wait_for_approve_message'][0][3:-4].replace('<br />', ''))

@dp.message_handler(lambda message: message.text.lower() == 'поиск', state='*')
async def cmd_search(message: types.Message):
    logging.info(f"Телеграм-пользователь {message.from_user.username} нажал на поиск")
    await SearchStatesGroup.category.set()
    a = await bot.send_message(message.from_user.id, 'ОК', reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(message.chat.id, a.message_id)
    await bot.send_message(message.from_user.id, 'Перейдите в категории', reply_markup=search_kb())


@dp.message_handler(content_types=['text'], state=BotStatesGroup.name)
async def load_brand(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text
        data['user'] = message.from_user.id
        data['username'] = message.from_user.username

    MESSAGES = await get_commands_list()
    if 'location_share' in MESSAGES:
        await bot.send_message(message.from_user.id, MESSAGES['location_share'][0][3:-4].replace('<br />', ''), reply_markup=get_location_keyboard())
    else:
        await create_command(key='location_share', text='Можете поделиться своей геопозицией:')
        MESSAGES = await get_commands_list()
        await bot.send_message(message.from_user.id, MESSAGES['location_share'][0][3:-4].replace('<br />', ''), reply_markup=get_location_keyboard())
    await BotStatesGroup.next()


@dp.message_handler(state=BotStatesGroup.location, content_types=types.ContentTypes.LOCATION)
async def load_location(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['location'] = await get_city_from_location(latitude=str(message.location['latitude']), longitude=str(message.location['longitude']))

    MESSAGES = await get_commands_list()
    a = await bot.send_message(message.from_user.id, "ОК", reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(message.chat.id, a.message_id)
    if 'company_name_message' in MESSAGES:
        await send_photo_with_url(TOKEN=TOKEN, CHAT_ID=str(message.from_user.id), img_url=MESSAGES['company_name_message'][1], caption=MESSAGES['company_name_message'][0].replace('<br />', ''), parse_mode=types.ParseMode.HTML, message=message)
    else:
        await create_command(key='company_name_message', text='Отлично! Теперь введите название вашей компании')
        MESSAGES = await get_commands_list()
        await send_photo_with_url(TOKEN=TOKEN, CHAT_ID=str(message.from_user.id), img_url=MESSAGES['company_name_message'][1], caption=MESSAGES['company_name_message'][0].replace('<br />', ''), parse_mode=types.ParseMode.HTML, message=message)

    await BotStatesGroup.next()


@dp.message_handler(lambda message: message.text.lower() == 'отказаться', state=BotStatesGroup.location)
async def decline_location(message: types.Message, state: FSMContext):
    # Здесь можно добавить логику, которая должна выполняться при отказе от геопозиции
    async with state.proxy() as data:
        data['location'] = None  # Просто пример, как можно обработать отказ

    a = await bot.send_message(message.from_user.id, "ОК", reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(message.chat.id, a.message_id)
    MESSAGES = await get_commands_list()
    if 'company_name_message' in MESSAGES:
        await send_photo_with_url(TOKEN=TOKEN, CHAT_ID=str(message.from_user.id), img_url=MESSAGES['company_name_message'][1], caption=MESSAGES['company_name_message'][0].replace('<br />', ''), parse_mode=types.ParseMode.HTML, message=message)
    else:
        await create_command(key='company_name_message', text='Отлично! Теперь введите название вашей компании')
        MESSAGES = await get_commands_list()
        await send_photo_with_url(TOKEN=TOKEN, CHAT_ID=str(message.from_user.id), img_url=MESSAGES['company_name_message'][1], caption=MESSAGES['company_name_message'][0].replace('<br />', ''), parse_mode=types.ParseMode.HTML, message=message)

    await BotStatesGroup.next()



@dp.message_handler(state=BotStatesGroup.company_name)
async def load_year(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['company_name'] = message.text

    MESSAGES = await get_commands_list()
    if 'get_phone_message' in MESSAGES:

        await message.reply(MESSAGES['get_phone_message'][0][3:-4].replace('<br />', ''), reply_markup=get_phone_kb())
    else:
        await create_command(key='get_phone_message', text='Номер телефона')
        MESSAGES = await get_commands_list()
        await message.reply(MESSAGES['get_phone_message'][0][3:-4].replace('<br />', ''), reply_markup=get_phone_kb())
    await BotStatesGroup.next()



@ dp.message_handler(state=BotStatesGroup.phone, content_types=types.ContentTypes.CONTACT)
async def load_phone(message: types.Message, state: FSMContext):
    user_telephone_num = message.contact.phone_number
    async with state.proxy() as data:
        data['phone'] = user_telephone_num
        # отправляем созданную заявку указанному телеграм-юзеру
        await bot.send_message(chat_id=int(admin_id), text=f"ID: {message.from_user.id}\nИмя: {data['name']}, Компания: {data['company_name']}\nГеопозиция: {data['location']}\nТелефон: {data['phone']}", reply_markup=activate_user_kb())

        await message.answer(f"Отправлено администратору:\n{data['name']}, {data['company_name']}\nГеопозиция: {data['location']}\n{data['phone']}", reply_markup=ReplyKeyboardRemove())

        await create_bot_user(name=data['name'], company_name=data['company_name'], city=data['location'], phone=data['phone'], user_id=data['user'], username=data['username'])

        await state.finish()


@dp.callback_query_handler(lambda query: query.data == 'yes', state="*")
@dp.callback_query_handler(lambda query: query.data == 'no', state="*")
async def activate_user_handler(callback_query: CallbackQuery, state: FSMContext):
    # Получаем текущий индекс элемента списка из FSM
    user = str(callback_query.message.text.split('\n')[0].split(': ')[1])
    MESSAGES = await get_commands_list()
    async with state.proxy() as data:
        # name = data['name']
        # company_name = data['company_name']
        if callback_query.data == 'yes':
            await state.finish()
            logging.info(f"Телеграм-пользователь {callback_query.from_user.username} был успешно зарегистрирован")
            await activate_user(user_id=user)
            if 'registration_approval' in MESSAGES:
                await bot.send_message(user, MESSAGES['registration_approval'][0][3:-4].replace('<br />', ''), reply_markup=get_categories_kb())
                await bot.send_message(admin_id, 'Успешно подтверждено!')
            else:
                await create_command(key='registration_approval', text='Ура! Авторизация прошла успешно! Теперь вы можете просматривать каталог спецтехники, узнавать об акциях и быть в курсе самых актуальных новостей компании!')
                MESSAGES = await get_commands_list()
                await bot.send_message(user, MESSAGES['registration_approval'][0][3:-4].replace('<br />', ''), reply_markup=get_categories_kb())
                await bot.send_message(admin_id, 'Успешно подтверждено!')

            #await bot.send_message(chat_id=user, text=MESSAGES['registration_approval'][0][3:-4], reply_markup=get_categories_kb())
            # await send_photo_with_url(TOKEN=TOKEN, CHAT_ID=user, img_url=MESSAGES['registration_approval'][1], caption=MESSAGES['registration_approval'][0], parse_mode=types.ParseMode.HTML, message=callback_query.message.text)
        elif callback_query.data == 'no':
            await state.finish()
            logging.info(f"Телеграм-пользователь {callback_query.from_user.username} был отклонён администратором")
            if 'registration_disapproval' in MESSAGES:
                await bot.send_message(user, MESSAGES['registration_disapproval'][0][3:-4].replace('<br />', ''))
                await bot.send_message(admin_id, 'Регистрация отклонена!')
            else:
                await create_command(key='registration_disapproval', text='Увы! Мы не можем пропустить вас дальше...')
                MESSAGES = await get_commands_list()
                await bot.send_message(user, MESSAGES['registration_disapproval'][0][3:-4].replace('<br />', ''))
                await bot.send_message(admin_id, 'Регистрация отклонена!')
            #await bot.send_message(chat_id=user, text=MESSAGES['registration_disapproval'][0][3:-4])
            # await send_photo_with_url(TOKEN=TOKEN, CHAT_ID=user, img_url=MESSAGES['registration_disapproval'][1], caption=MESSAGES['registration_disapproval'][0], parse_mode=types.ParseMode.HTML, message=callback_query.message.text)


@dp.callback_query_handler(lambda query: query.data == 'manager', state="*")
async def activate_user_handler(callback_query: CallbackQuery, state: FSMContext):
    user = callback_query.message['chat']['id']
    message_text = callback_query.message.text
    username_match = re.search(r'username:\s*(\S+)', message_text)
    password_match = re.search(r'password:\s*(\S+)', message_text)
    username = username_match.group(1)
    password = password_match.group(1)
    MESSAGES = await get_commands_list()

    await save_manager(username=username, password=password, bot_user_id=callback_query.from_user.id)
    logging.info(f"Телеграм-пользователь {callback_query.from_user.username} был поставлен менеджером")
    if 'become_manager_message' in MESSAGES:
        await bot.send_message(user, MESSAGES['become_manager_message'][0][3:-4].replace('<br />', ''))
        await bot.send_message(admin_id, f'{callback_query.from_user.username} теперь менеджер!')
    else:
        await create_command(key='become_manager_message', text='Поздравляем! Теперь вы менеджер')
        MESSAGES =await get_commands_list()
        await bot.send_message(user, MESSAGES['become_manager_message'][0][3:-4].replace('<br />', ''))
        await bot.send_message(admin_id, f'{callback_query.from_user.username} теперь менеджер!')
    #await bot.send_message(chat_id=user, text=MESSAGES['become_manager_message'][0][3:-4])
    #await send_photo_with_url(TOKEN=TOKEN, CHAT_ID=user, img_url=MESSAGES['become_manager_message'][1], caption=MESSAGES['become_manager_message'][0], parse_mode=types.ParseMode.HTML, message=callback_query.message.text)


@dp.callback_query_handler(lambda query: query.data == 'post', state="*")
async def post_handler(callback_query: CallbackQuery, state: FSMContext):
    admin = callback_query.message['chat']['id']
    message = callback_query.message.text.split('\n')
    t = datetime.datetime(2023, 8, 25, 12, 49, tzinfo=datetime.timezone.utc)
    await change_post_status(message[0].split(': ')[1])
    time = message[-1].split(': ')[1].split(' (')[1].split('|запланировано на ')[1][:-1]
    if time!='None':
        asyncio.create_task(schedule_mailing(message=message, time=time))
    else:
        await do_mailing(message)
    logging.info(f"Пост {message[0].split(': ')[1]} был одобрен на рассылку админом")
    await bot.send_message(chat_id=admin, text=f"Рассылка поста {message[0].split(': ')[1]} одобрена!")
    await bot.send_message(chat_id=message[-1].split(': ')[1].split(' ')[0], text=f"Рассылка поста {message[0].split(': ')[1]} одобрена!")


@dp.callback_query_handler(lambda query: query.data == 'no_post', state="*")
async def no_post_handler(callback_query: CallbackQuery, state: FSMContext):
    admin = callback_query.message['chat']['id']
    message = callback_query.message.text.split('\n')
    manager_id = message[-1].split(': ')[1].split(' ')[0]
    logging.info(f"Пост {message[0].split(': ')[1]} не был одобрен на рассылку админом")
    await bot.send_message(chat_id=manager_id, text=f"Рассылка поста {message[0].split(': ')[1]} отклонена!")

@dp.callback_query_handler(lambda query: query.data == 'poll', state="*")
async def activate_user_handler(callback_query: CallbackQuery, state: FSMContext):
    user = callback_query.message['chat']['id']
    poll = callback_query.message.text.split('\n')
    message = callback_query.message.text.split('\n')
    time = message[-1].split(': ')[1].split(' (')[1].split('|запланировано на ')[1][:-1]
    await change_poll_status(poll[0].split(': ')[1])
    if time!='None':
        asyncio.create_task(schedule_poll_mailing(message=message, time=time))
    else:
        print('check')
        await do_poll_mailing(message)

    logging.info(f"Опрос {message[0].split(': ')[1]} был одобрен на рассылку админом")
    await bot.send_message(chat_id=user, text=f"Рассылка опроса {message[0]} одобрена!")
    await bot.send_message(chat_id=poll[-1].split(': ')[1].split(' ')[0], text=f"Рассылка опроса {message[0].split(': ')[1]} одобрена!")

@dp.callback_query_handler(lambda query: query.data == 'no_poll', state="*")
async def no_post_handler(callback_query: CallbackQuery, state: FSMContext):
    admin = callback_query.message['chat']['id']
    message = callback_query.message.text.split('\n')
    manager_id = message[-1].split(': ')[1].split(' ')[0]
    logging.info(f"Опрос {message[0].split(': ')[1]} не был одобрен на рассылку админом")
    await bot.send_message(chat_id=manager_id, text=f"Рассылка опроса {message[0].split(': ')[1]} отклонена!")


@dp.callback_query_handler(lambda query: query.data == 'storynews', state="*")
async def activate_user_handler(callback_query: CallbackQuery, state: FSMContext):
    admin = callback_query.message['chat']['id']
    try:
        item = callback_query.message.text.split('\n')[0].split(': ')[1]
        item_id = callback_query.message.text.split('\n')[0].split(': ')[1]
        await create_storynews_views(item_id)
        user = callback_query.message.text.split('\n')[-1].split(': ')[1].split(' ')[0]
    except:
        item = callback_query.message.caption.split('\n')[0].split(': ')[1]
        item_id = callback_query.message.caption.split('\n')[0].split(': ')[1]
        await create_storynews_views(item_id)
        user = callback_query.message.caption.split('\n')[-1].split(': ')[1].split(' ')[0]
    await change_storynews_status(item)
    logging.info(f"Актуальное/новость {item_id} была одобрена на рассылку админом")
    await bot.send_message(chat_id=user, text=f"Новость/актуальное {item_id} одобрено!")
    await bot.send_message(chat_id=admin, text=f"Новость/актуальное {item_id} одобрено!")

@dp.callback_query_handler(lambda query: query.data == 'no_storynews', state="*")
async def activate_user_handler(callback_query: CallbackQuery, state: FSMContext):
    logging.info(f"Актуальное/новость {item_id} не была одобрена на рассылку админом")
    try:
        user = callback_query.message.text.split('\n')[-1].split(': ')[1].split(' ')[0]
        item_id = callback_query.message.text.split('\n')[0].split(': ')[1]
        await bot.send_message(chat_id= user, text=f"Новость/актуальное {item_id} отклонено!")
    except:
        user = callback_query.message.caption.split('\n')[-1].split(': ')[1].split(' ')[0]
        item_id = callback_query.message.caption.split('\n')[0].split(': ')[1]
        await bot.send_message(chat_id= user, text=f"Новость/актуальное {item_id} отклонено!")


@dp.message_handler()
async def cmd_catalog(message: types.Message, state: FSMContext) -> None:
    await send_last_interaction(str(message.from_user.id))
    if await check_botuser_activated(str(message.from_user.id)):
        if message.text=='Каталог':
            a = await bot.send_message(message.from_user.id, "OK", reply_markup=ReplyKeyboardRemove())
            await bot.delete_message(message.chat.id, a.message_id)
            logging.info(f"Телеграм-пользователь {message.from_user.username} просматривает каталог...")
            data = await state.get_data()
            child = message.text
            new_categories = []


            data['ALL_CATEGORIES'] = await get_categories_list()
            data['CATEGORIES'] = data['ALL_CATEGORIES'][:]

            CATEGORIES = data['CATEGORIES']
            catalog_id = [i for i in CATEGORIES if i['parent']==None][0]['id']
            new_categories = await find_children(CATEGORIES, child)

            data['CATEGORIES'] = new_categories


            sent_message = await message.answer("Выберите категорию:", reply_markup=create_category_keyboard_with_menu([i for i in new_categories if i['parent'] == catalog_id]))
            await bot.delete_message(message.chat.id, message.message_id)
            data['message_id'] = sent_message.message_id
            await state.set_data(data)

        elif message.text=='О нас':
            logging.info(f"Телеграм-пользователь {message.from_user.username} смотрит вкладку 'О нас' ")
            MESSAGES = await get_commands_list()
            if 'about_us_message' in MESSAGES:
                await send_photo_with_url(TOKEN=TOKEN, CHAT_ID=str(message.from_user.id), img_url=MESSAGES['about_us_message'][1], caption=MESSAGES['about_us_message'][0].replace('<br />', ''), parse_mode=types.ParseMode.HTML, message=message)
            else:
                await create_command(key='about_us_message', text='Мы хорошая компания!')
                MESSAGES = await get_commands_list()
                await send_photo_with_url(TOKEN=TOKEN, CHAT_ID=str(message.from_user.id), img_url=MESSAGES['about_us_message'][1], caption=MESSAGES['about_us_message'][0].replace('<br />', ''), parse_mode=types.ParseMode.HTML, message=message)

        elif message.text=='Новости':
            a = await bot.send_message(message.from_user.id, "OK", reply_markup=ReplyKeyboardRemove())
            await bot.delete_message(message.chat.id, a.message_id)
            logging.info(f"Телеграм-пользователь {message.from_user.username} просматривает новости")
            data_list = await get_news_or_stories_list('news')
            await bot.delete_message(message.chat.id, message.message_id)

            if data_list:
                # Сохраняем список продуктов и текущий индекс элемента в FSM
                async with state.proxy() as data:
                    data['items'] = data_list
                    data['current_index'] = 0

                    item = data_list[0]
                    await create_storynews_views(item["id"])
                    photo = await download_photo(item["photo"])
                    if not photo:
                        a = await message.answer(f"{item['name']}:\n{item['description']}", reply_markup=get_items_kb(data_list))
                    else:
                        a = await bot.send_photo(message.from_user.id, photo, caption=f'{item["name"]} - {item["description"]}', reply_markup=get_items_kb(data_list))
                    data['item_message_id'] = a.message_id
                    data['item_name'] = item['name']
                    data['item_description'] = item['description']

            else:
                await bot.send_message(message.from_user.id, f"Список новостей пуст.", reply_markup=get_menu_keyboard())

        #   Устанавливаем состояние ProductState.current_index для перехода к обработке кнопок навигации
            # await ItemState.current_index.set()

        elif message.text=='Актуальное':
            a = await bot.send_message(message.from_user.id, "OK", reply_markup=ReplyKeyboardRemove())
            await bot.delete_message(message.chat.id, a.message_id)
            logging.info(f"Телеграм-пользователь {message.from_user.username} просматривает актуальное")
            data_list = await get_news_or_stories_list('stories')
            await bot.delete_message(message.chat.id, message.message_id)

            if data_list:
                # Сохраняем список продуктов и текущий индекс элемента в FSM
                async with state.proxy() as data:
                    data['items'] = data_list
                    data['current_index'] = 0

                    item = data_list[0]
                    await create_storynews_views(item["id"])

                    photo = await download_photo(item["photo"])
                    if not photo:
                        a = await message.answer(f"{item['name']}:\n{item['description']}", reply_markup=get_items_kb(data_list))
                    else:
                        a = await bot.send_photo(message.from_user.id, photo, caption=f'{item["name"]} - {item["description"]}', reply_markup=get_items_kb(data_list))
                    data['item_message_id'] = a.message_id
                    data['item_name'] = item['name']
                    data['item_description'] = item['description']

            else:
                await bot.send_message(message.from_user.id, f"Список актуального пуст.", reply_markup=get_menu_keyboard())


        elif message.text=='Акции':
            data_list = await get_promotions_list()
            a = await bot.send_message(message.from_user.id, "OK", reply_markup=ReplyKeyboardRemove())
            await bot.delete_message(message.chat.id, a.message_id)
            logging.info(f"Телеграм-пользователь {message.from_user.username} просматривает акции")

            if data_list:
                # Сохраняем список продуктов и текущий индекс элемента в FSM
                async with state.proxy() as data:
                    data['promotions'] = data_list
                    data['promotion_index'] = 0

                    promotion = data_list[0]

                    photo = await download_photo(promotion["photo"])
                    price = '{:,.0f}'.format(float(promotion['price'])).replace(',', ' ')
                    media = await get_product_media(str(promotion['id']))
                    kp = await get_kp_path(str(promotion['id']))
                    print(kp)
                    if not photo:
                        s = f"<b>ID товара</b>: {promotion['id']}\n<b>Название</b>: {promotion['name']}\n<b>Описание</b>: {promotion['promotion_description']}\n<b>Марка</b>: {promotion['brand']}\n<b>Модель</b>: {promotion['product_model']}\n<b>Комплектация</b>: {promotion['equipment']}\n<b>Производитель</b>: {promotion['manufacturer']}\n<b>Год выпуска</b>: {promotion['year']}\n<b>Стоимость</b>: {price} {promotion['currency']}\n<b>Статус</b>: {promotion['status']}"
                        filtered_lines = [line for line in s.split('\n') if line.split(':')[1] not in (' None', ' ')]
                        result = '\n'.join(filtered_lines)
                        a = await message.answer(result.replace('None', '')+'\n\nАкция!', reply_markup=get_promotions_kb(media, data_list, kp), parse_mode=types.ParseMode.HTML)
                    else:
                        s = f"<b>ID товара</b>: {promotion['id']}\n<b>Название</b>: {promotion['name']}\n<b>Описание</b>: {promotion['promotion_description']}\n<b>Марка</b>: {promotion['brand']}\n<b>Модель</b>: {promotion['product_model']}\n<b>Комплектация</b>: {promotion['equipment']}\n<b>Производитель</b>: {promotion['manufacturer']}\n<b>Год выпуска</b>: {promotion['year']}\n<b>Стоимость</b>: {price} {promotion['currency']}\n<b>Статус</b>: {promotion['status']}"
                        filtered_lines = [line for line in s.split('\n') if line.split(':')[1] not in (' None', ' ')]
                        result = '\n'.join(filtered_lines)
                        a = await bot.send_photo(message.from_user.id, photo, caption=result.replace('None', '')+'\n\nАкция!', reply_markup=get_promotions_kb(media, data_list, kp), parse_mode=types.ParseMode.HTML)

                    data['promotion_message_id'] = a.message_id
                    data['promotion_name'] = promotion['name']
                    data['promotion_description'] = promotion['promotion_description']

            else:
                await bot.send_message(message.from_user.id, f"Список акций пуст.", reply_markup=get_menu_keyboard())

    else:
        MESSAGES = await get_commands_list()
        if 'wait_for_approve_message' in MESSAGES:
            await bot.send_message(message.from_user.id, MESSAGES['wait_for_approve_message'][0][3:-4].replace('<br />', ''))
        else:
            await create_command(key='wait_for_approve_message', text='Пользователь не подтверждён')
            MESSAGES = await get_commands_list()
            await bot.send_message(message.from_user.id, MESSAGES['wait_for_approve_message'][0][3:-4].replace('<br />', ''))

        # await send_photo_with_url(TOKEN=TOKEN, CHAT_ID=str(message.from_user.id), img_url=MESSAGES['wait_for_approve_message'][1], caption=MESSAGES['wait_for_approve_message'][0], parse_mode=types.ParseMode.HTML, message=message)




@dp.callback_query_handler(lambda query: query.data == 'menu', state='*')
async def callback_menu(callback_query: CallbackQuery, state: FSMContext):
    logging.info(f"Телеграм-пользователь {callback_query.from_user.username} нажал на меню")
    # Ваш код для обработки callback_data='menu' здесь
    await state.finish()
    # Удаляем inline-клавиатуру
    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )

    # Отправляем новую reply-клавиатуру
    sent_message = await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text="Выберите опцию",
        reply_markup=get_categories_kb()
    )

    # await asyncio.sleep(4)

    # await bot.delete_message(
    #     chat_id=callback_query.message.chat.id,
    #     message_id=sent_message.message_id,
    # )

@dp.callback_query_handler(lambda query: query.data == 'manager_chat', state='*')
async def callback_chat_with_manager(callback_query: CallbackQuery):
    logging.info(f"Телеграм-пользователь {callback_query.from_user.username} нажал на 'Чат с менеджером'")

    if callback_query.message.caption:
        product = callback_query.message.caption.split('\n')[1]
        product_id = callback_query.message.caption.split('\n')[0].split(': ')[1]
    else:
        product = callback_query.message.text.split('\n')[1]
        product_id = callback_query.message.text.split('\n')[0].split(': ')[1]
    await create_product_chat(str(product_id))
    product_link = f"{domen}admin/products/product/{product_id}/change/"
    bot_user = callback_query.from_user.id
    print(bot_user)
    phone = await search_user_by_id(bot_user)
    try:
        manager_telegram_username = await get_manager_with_category(product_id=str(product_id))
        await create_manager_request(product=f'{product} {product_link}', bot_user=bot_user, manager=manager_telegram_username)
        await bot.send_message(callback_query.from_user.id, f"@{manager_telegram_username}")

        await bot.send_message(int(manager_telegram_username['user_id']), f"Запросил Чат: @{callback_query.from_user.username}\nТелефон: {phone['phone']}")
    except:
        await bot.send_message(int(admin_id), f"Запросил Чат: @{callback_query.from_user.username}\nТелефон: {phone['phone']}")



@dp.callback_query_handler(lambda query: query.data == 'kp', state='*')
async def callback_kp_request(callback_query: CallbackQuery):
    logging.info(f"Телеграм-пользователь {callback_query.from_user.username} нажал на 'Запрос на КП'")
    if callback_query.message.caption:
        text = callback_query.message.caption
    else:
        text = callback_query.message.text
    # await BotStatesGroup.name.set()
    if callback_query.message.caption:
        product = callback_query.message.caption.split('\n')[1]
        product_id = callback_query.message.caption.split('\n')[0].split(': ')[1]
    else:
        product = callback_query.message.text.split('\n')[1]
        product_id = callback_query.message.text.split('\n')[0].split(': ')[1]
    manager_telegram_username = await get_manager_with_category(product_id=str(product_id))
    await create_product_kp(str(product_id))
    MESSAGES = await get_commands_list()
    # await create_profile(user_id=message.from_user.id)
    if 'kp_sent_message' in MESSAGES:
        await send_photo_with_url(TOKEN=TOKEN, CHAT_ID=str(callback_query.from_user.id), img_url=MESSAGES['kp_sent_message'][1], caption=MESSAGES['kp_sent_message'][0].replace('<p>', '').replace('</p>', '').replace('<br />', '')+f'\nЧат с менеджером: @{manager_telegram_username}', parse_mode=types.ParseMode.HTML, message=callback_query)
    else:
        await create_command(key='kp_sent_message', text='Запрос сформирован, скоро с Вами свяжутся')
        MESSAGES = await get_commands_list()
        await send_photo_with_url(TOKEN=TOKEN, CHAT_ID=str(callback_query.from_user.id), img_url=MESSAGES['kp_sent_message'][1], caption=MESSAGES['kp_sent_message'][0].replace('<p>', '').replace('</p>', '').replace('<br />', '')+f'\nЧат с менеджером: @{manager_telegram_username}', parse_mode=types.ParseMode.HTML, message=callback_query)
    user = callback_query.from_user.id
    path = await get_kp_path(product_id)
    phone = await search_user_by_id(user)
    if path:
        with open(path, 'rb') as file:
            await bot.send_document(callback_query.from_user.id, InputFile(file))
    else:
        await bot.send_message(callback_query.from_user.id, 'Менеджер скоро с вами свяжется')
    product_link = f"{domen}admin/products/product/{product_id}/change/"
    await create_kp_request(product=f'{product} {product_link}', bot_user=user, manager=manager_telegram_username)
    try:
        d = await search_manager_id(manager_telegram_username)
        await bot.send_message(int(d['user_id']), f"{text}\nЗапросил КП: @{callback_query.from_user.username}\nТелефон: {phone['phone']}")
    except:
        await bot.send_message(int(admin_id), f"{text}\nЗапросил КП: @{callback_query.from_user.username}\nТелефон: {phone['phone']}")


@dp.callback_query_handler(lambda query: query.data == 'media', state="*")
async def media_handler(callback_query: CallbackQuery, state: FSMContext):
    logging.info(f"Телеграм-пользователь {callback_query.from_user.username} нажал на 'Показать ещё'")
    user = callback_query.message['chat']['id']
    product_id = callback_query.message.caption.split('\n')[0].split(': ')[1]
    photo_pathes = await get_product_media(product_id)
    media_group = [InputMediaPhoto(media=types.InputFile(rf'{path}')) for path in photo_pathes]
    try:
        await bot.send_media_group(user, media=media_group)
    except:
        await bot.send_message(user, 'Дополнительные фото отсутствуют')



@dp.callback_query_handler(lambda query: query.data == 'next_promotion', state='*')
@dp.callback_query_handler(lambda query: query.data == 'previous_promotion', state='*')
async def promotions_navigation(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as current_data:
        promotions = current_data.get('promotions', [])
        current_index = current_data.get('promotion_index', 0)

        if callback_query.data == 'previous_promotion':
            # if current_index!=0:
            current_index -= 1
        elif callback_query.data == 'next_promotion':
            current_index += 1

        current_data['promotion_index'] = current_index


        try:
            promotion = promotions[current_index]
            photo = await download_photo(promotion["photo"])
            # if current_data['promotion_description'] in (None, '') and promotion['promotion_description'] in (None, ''):
            #     success = bool(current_data['promotion_name'] != promotion['name'])
            # else:
            #     success = bool(current_data['promotion_name'] != promotion['name'] and current_data['promotion_description'] != promotion['promotion_description'])
            # if success:
            price = '{:,.0f}'.format(float(promotion['price'])).replace(',', ' ')
            media = await get_product_media(str(promotion['id']))
            kp = await get_kp_path(str(promotion['id']))
            if not photo:
                s = f"<b>ID товара</b>: {promotion['id']}\n<b>Название</b>: {promotion['name']}\n<b>Описание</b>: {promotion['promotion_description']}\n<b>Марка</b>: {promotion['brand']}\n<b>Модель</b>: {promotion['product_model']}\n<b>Комплектация</b>: {promotion['equipment']}\n<b>Производитель</b>: {promotion['manufacturer']}\n<b>Год выпуска</b>: {promotion['year']}\n<b>Стоимость</b>: {price} {promotion['currency']}\n<b>Статус</b>: {promotion['status']}"
                filtered_lines = [line for line in s.split('\n') if line.split(':')[1] not in (' None', ' ')]
                result = '\n'.join(filtered_lines)
                a = await bot.send_message(callback_query.from_user.id, result.replace('None', '')+'\n\nАкция!', reply_markup=get_promotions_kb(media, promotions, kp), parse_mode=types.ParseMode.HTML)
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=current_data['promotion_message_id'])
                current_data['promotion_message_id'] = a.message_id
            else:
                s = f"<b>ID товара</b>: {promotion['id']}\n<b>Название</b>: {promotion['name']}\n<b>Описание</b>: {promotion['promotion_description']}\n<b>Марка</b>: {promotion['brand']}\n<b>Модель</b>: {promotion['product_model']}\n<b>Комплектация</b>: {promotion['equipment']}\n<b>Производитель</b>: {promotion['manufacturer']}\n<b>Год выпуска</b>: {promotion['year']}\n<b>Стоимость</b>: {price} {promotion['currency']}\n<b>Статус</b>: {promotion['status']}"
                filtered_lines = [line for line in s.split('\n') if line.split(':')[1] not in (' None', ' ')]
                result = '\n'.join(filtered_lines)
                a = await bot.send_photo(callback_query.from_user.id, photo, caption=result.replace('None', '')+'\n\nАкция!', reply_markup=get_promotions_kb(media, promotions, kp), parse_mode=types.ParseMode.HTML)
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=current_data['promotion_message_id'])
                current_data['promotion_message_id'] = a.message_id

            current_data['promotion_name'] = promotion['name']
            current_data['promotion_description'] = promotion['promotion_description']
            # else:
            #     await callback_query.answer("Достигнут край списка акций.", show_alert=True)
        except:
            if current_index == len(promotions):
                current_data['promotion_index'] = 0
                promotion = promotions[0]
            else:
                current_data['promotion_index'] = len(promotions)
                promotion = promotions[len(promotions)-1]
            photo = await download_photo(promotion["photo"])
            # if current_data['promotion_description'] in (None, '') and promotion['promotion_description'] in (None, ''):
            #     success = bool(current_data['promotion_name'] != promotion['name'])
            # else:
            #     success = bool(current_data['promotion_name'] != promotion['name'] and current_data['promotion_description'] != promotion['promotion_description'])
            # if success:
            price = '{:,.0f}'.format(float(promotion['price'])).replace(',', ' ')
            media = await get_product_media(str(promotion['id']))
            kp = await get_kp_path(str(promotion['id']))
            if not photo:
                s = f"<b>ID товара</b>: {promotion['id']}\n<b>Название</b>: {promotion['name']}\n<b>Описание</b>: {promotion['promotion_description']}\n<b>Марка</b>: {promotion['brand']}\n<b>Модель</b>: {promotion['product_model']}\n<b>Комплектация</b>: {promotion['equipment']}\n<b>Производитель</b>: {promotion['manufacturer']}\n<b>Год выпуска</b>: {promotion['year']}\n<b>Стоимость</b>: {price} {promotion['currency']}\n<b>Статус</b>: {promotion['status']}"
                filtered_lines = [line for line in s.split('\n') if line.split(':')[1] not in (' None', ' ')]
                result = '\n'.join(filtered_lines)
                a = await bot.send_message(callback_query.from_user.id, result.replace('None', '')+'\n\nАкция!', reply_markup=get_promotions_kb(media, promotions, kp), parse_mode=types.ParseMode.HTML)
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=current_data['promotion_message_id'])
                current_data['promotion_message_id'] = a.message_id
            else:
                s = f"<b>ID товара</b>: {promotion['id']}\n<b>Название</b>: {promotion['name']}\n<b>Описание</b>: {promotion['promotion_description']}\n<b>Марка</b>: {promotion['brand']}\n<b>Модель</b>: {promotion['product_model']}\n<b>Комплектация</b>: {promotion['equipment']}\n<b>Производитель</b>: {promotion['manufacturer']}\n<b>Год выпуска</b>: {promotion['year']}\n<b>Стоимость</b>: {price} {promotion['currency']}\n<b>Статус</b>: {promotion['status']}"
                filtered_lines = [line for line in s.split('\n') if line.split(':')[1] not in (' None', ' ')]
                result = '\n'.join(filtered_lines)
                a = await bot.send_photo(callback_query.from_user.id, photo, caption=result.replace('None', '')+'\n\nАкция!', reply_markup=get_promotions_kb(media, promotions, kp), parse_mode=types.ParseMode.HTML)
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=current_data['promotion_message_id'])
                current_data['promotion_message_id'] = a.message_id

            current_data['promotion_name'] = promotion['name']
            current_data['promotion_description'] = promotion['promotion_description']
            # else:
            #     await callback_query.answer("Достигнут край списка акций.", show_alert=True)

@dp.callback_query_handler(lambda query: query.data == 'next_item', state="*")
@dp.callback_query_handler(lambda query: query.data == 'previous_item', state="*")
async def process_news_or_stories_navigation(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as current_data:
        items = current_data.get('items', [])
        current_index = current_data.get('current_index', 0)

        if callback_query.data == 'previous_item':
            # if current_index!=0:
            current_index -= 1
        elif callback_query.data == 'next_item':
            current_index += 1

        current_data['current_index'] = current_index


        try:
            item = items[current_index]
            await create_storynews_views(item["id"])
            photo = await download_photo(item["photo"])
            #if current_data['item_name'] != item['name'] and current_data['item_description'] != item['description']:
            if not photo:
                a = await bot.send_message(callback_query.from_user.id, f"{item['name']}:\n{item['description']}".replace('None', ''), reply_markup=get_items_kb(items))
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=current_data['item_message_id'])
                current_data['item_message_id'] = a.message_id
            else:
                a = await bot.send_photo(callback_query.from_user.id, photo, caption=f'{item["name"]} - {item["description"]}'.replace('None', ''), reply_markup=get_items_kb(items))
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=current_data['item_message_id'])
                current_data['item_message_id'] = a.message_id

            current_data['item_name'] = item['name']
            current_data['item_description'] = item['description']
            # else:
            #     await callback_query.answer("Достигнут край списка новостей/актуальных.", show_alert=True)
        except:
            if current_index == len(items):
                current_data['current_index'] = 0
                item = items[0]
            else:
                current_data['current_index'] = len(items)-1
                item = items[len(items)-1]

            await create_storynews_views(item["id"])
            photo = await download_photo(item["photo"])
            # if current_data['item_name'] != item['name'] and current_data['item_description'] != item['description']:
            if not photo:
                a = await bot.send_message(callback_query.from_user.id, f"{item['name']}:\n{item['description']}".replace('None', ''), reply_markup=get_items_kb(items))
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=current_data['item_message_id'])
                current_data['item_message_id'] = a.message_id
            else:
                a = await bot.send_photo(callback_query.from_user.id, photo, caption=f'{item["name"]} - {item["description"]}'.replace('None', ''), reply_markup=get_items_kb(items))
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=current_data['item_message_id'])
                current_data['item_message_id'] = a.message_id

            current_data['item_name'] = item['name']
            current_data['item_description'] = item['description']
            # else:
            #     await callback_query.answer("Достигнут край списка новостей/актуальных.", show_alert=True)

@dp.callback_query_handler(lambda query: query.data == 'models', state='*')
async def menu_product_navigation(callback_query: CallbackQuery, state: FSMContext):
    logging.info(f"Телеграм-пользователь {callback_query.from_user.username} нажал на меню")
    await state.finish()
    a = await bot.send_message(callback_query.from_user.id, text="Выберите опцию", reply_markup=get_categories_kb())
    await asyncio.sleep(4)

    # await bot.delete_message(
    #     chat_id=callback_query.message.chat.id,
    #     message_id=a.message_id,
    # )
    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )


@dp.callback_query_handler(lambda query: query.data == 'Каталог', state=SearchStatesGroup.category)
async def search(callback_query: CallbackQuery, state: FSMContext) -> None:
    if await check_botuser_activated(str(callback_query.from_user.id)):
        data = await state.get_data()
        child = callback_query.data
        new_categories = []


        data['ALL_CATEGORIES'] = await get_categories_list()
        data['CATEGORIES'] = data['ALL_CATEGORIES'][:]

        CATEGORIES = data['CATEGORIES']
        catalog_id = [i for i in CATEGORIES if i['parent']==None][0]['id']
        new_categories = await find_children(CATEGORIES, child)

        data['CATEGORIES'] = new_categories


        sent_message = await bot.send_message(callback_query.from_user.id, "Выберите категорию:", reply_markup=create_category_keyboard_with_menu([i for i in new_categories if i['parent'] == catalog_id]))
        #await bot.delete_message(callback_query.from_user.id, callback_query.message_id)
        data['message_id'] = sent_message.message_id
        await state.set_data(data)

    else:
        MESSAGES = await get_commands_list()
        if 'wait_for_approve_message' in MESSAGES:
            await bot.send_message(callback_query.from_user.id, MESSAGES['wait_for_approve_message'][0][3:-4].replace('<br />', ''))
        else:
            await create_command(key='wait_for_approve_message', text='Пользователь не подтверждён')
            MESSAGES = await get_commands_list()
            await bot.send_message(callback_query.from_user.id, MESSAGES['wait_for_approve_message'][0][3:-4].replace('<br />', ''))





@dp.callback_query_handler(lambda query: True, state=SearchStatesGroup.category)
async def callback_search_category(callback_query: CallbackQuery, state: FSMContext):
    parent_id = callback_query.data
    data = await state.get_data()
    new_categories = []

    if not data.get('CATEGORIES'):
        data['ALL_CATEGORIES'] = await get_categories_list()
        data['CATEGORIES'] = data['ALL_CATEGORIES'][:]

    CATEGORIES = data['CATEGORIES']
    child = [i['name'] for i in CATEGORIES if str(i['id']) == str(parent_id)][0]
    new_categories = await find_children(CATEGORIES, child)
    child_id = [i["id"] for i in data['CATEGORIES'] if i["name"] == child][0]


    if type(new_categories)==list and len(new_categories):
        data['CATEGORIES'] = new_categories
        message_id = data['message_id']

        try:
            await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=message_id, reply_markup=create_category_keyboard_with_menu([i for i in new_categories if i['parent'] == child_id]))
        except:
            None


    else:
        category_id = int(new_categories)
        data_list = await get_products_list(category_id=category_id)
        for item in data_list:
            for key, value in item.items():
                if value is None:
                    item[key] = 'None'
        await state.update_data(data_list=data_list)


        await SearchStatesGroup.next()
        await SearchStatesGroup.wow.set()

        await bot.send_message(callback_query.from_user.id, 'Перейдём к фильтрам', reply_markup=filters(data_list))


    # message_id = data['message_id']

    # try:
    #     await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=message_id, reply_markup=create_category_keyboard_with_menu([i for i in new_categories if i['parent'] == child_id]))
    # except:
    #     None



@dp.callback_query_handler(lambda query: True, state=SearchStatesGroup.wow)
async def process_wow(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(selected_species=callback_query.data)
    async with state.proxy() as data:
        data_list = data.get("data_list")
        message_id = data['message_id']
        sent_message = await bot.send_message(callback_query.from_user.id, 'фильтрация по стране производителя', reply_markup=country(data_list))
        data['message_id'] = sent_message.message_id
        # await bot.send_message(callback_query.from_user.id, "Выберите вид:", reply_markup=species(data_list))
    await SearchStatesGroup.next()


@dp.callback_query_handler(lambda query: True, state=SearchStatesGroup.species)
async def process_species(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(selected_species=callback_query.data)
    async with state.proxy() as data:
        data_list = data.get("data_list")
        message_id = data['message_id']
        sent_message = await bot.send_message(chat_id=callback_query.message.chat.id, text="фильтрация по колёсной формуле", reply_markup=wheels(data_list))
        data['message_id'] = sent_message.message_id
        # await bot.send_message(callback_query.from_user.id, "Выберите колеса:", reply_markup=wheels(data_list))
    await SearchStatesGroup.next()


@dp.callback_query_handler(lambda query: True, state=SearchStatesGroup.wheels)
async def process_wheels(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(selected_wheels=callback_query.data)
    async with state.proxy() as data:
        data_list = data.get("data_list")
        message_id = data['message_id']
        sent_message = await bot.send_message(chat_id=callback_query.message.chat.id, text="фильтрация по марке", reply_markup=brand(data_list))
        data['message_id'] = sent_message.message_id
        # await bot.send_message(callback_query.from_user.id,"Выберите марку:", reply_markup=brand(data_list))
    await SearchStatesGroup.next()


@dp.callback_query_handler(lambda query: True, state=SearchStatesGroup.brand)
async def process_brand(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(selected_brand=callback_query.data)
    async with state.proxy() as data:
        data_list = data.get("data_list")
        message_id = data['message_id']
        sent_message = await bot.send_message(chat_id=callback_query.message.chat.id, text="фильтрация по виду", reply_markup=species(data_list))
        data['message_id'] = sent_message.message_id
        # await bot.send_message(callback_query.from_user.id,"Выберите страну производителя:", reply_markup=country(data_list))
    await SearchStatesGroup.next()

@dp.callback_query_handler(lambda query: True, state=SearchStatesGroup.country)
async def process_brand(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(selected_country=callback_query.data)
    async with state.proxy() as data:
        data_list = data.get("data_list")
        message_id = data['message_id']
        sent_message = await bot.send_message(chat_id=callback_query.message.chat.id, text="фильтрация по году", reply_markup=year(data_list))
        data['message_id'] = sent_message.message_id
        # await bot.send_message(callback_query.from_user.id,"Выберите год:", reply_markup=year(data_list))
    await SearchStatesGroup.next()



@dp.callback_query_handler(lambda query: query.data == 'next', state='*')
@dp.callback_query_handler(lambda query: query.data == 'previous', state='*')
async def process_product_navigation(callback_query: CallbackQuery, state: FSMContext):
    # Получаем текущий индекс элемента списка из FSM
    async with state.proxy() as current_data:
        try:
            await bot.delete_message(chat_id=callback_query.message.chat.id,message_id=current_data['message_id'])
        except:
            None
        products = current_data.get('products', [])
        current_index = current_data.get('current_index', 0)

        if callback_query.data == 'previous':
            # if current_index!=0:
            current_index -= 1
        if callback_query.data == 'next':
            current_index += 1


        current_data['current_index'] = current_index


        try:
            product = products[current_index]
            await create_product_views(product["id"])
            photo = await download_photo(product["photo"])
            #if current_data['product_name'] != product['name'] and str(current_data['product_price']) != str(product['price']):
            promotion = '\n\nАкция!' if product['promotion'] else ''
            price = '{:,.0f}'.format(float(product['price'])).replace(',', ' ')
            media = await get_product_media(str(product['id']))
            kp = await get_kp_path(product['id'])
            if photo:
                s = f"<b>ID товара</b>: {product['id']}\n<b>Название</b>: {product['name']}\n<b>Описание</b>: {product['description']}\n<b>Марка</b>: {product['brand']}\n<b>Модель</b>: {product['product_model']}\n<b>Комплектация</b>: {product['equipment']}\n<b>Производитель</b>: {product['manufacturer']}\n<b>Год выпуска</b>: {product['year']}\n<b>Стоимость</b>: {price} {product['currency']}\n<b>Статус</b>: {product['status']}"
                filtered_lines = [line for line in s.split('\n') if line.split(':')[1] not in (' None', ' ')]
                result = '\n'.join(filtered_lines)
                a = await bot.send_photo(callback_query.from_user.id, photo, caption=result.replace('None', '')+promotion, reply_markup=get_product_kb(media, products, kp), parse_mode=types.ParseMode.HTML)
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=current_data['product_message_id'])
                current_data['product_message_id'] = a.message_id
            else:
                s = f"<b>ID товара</b>: {product['id']}\n<b>Название</b>: {product['name']}\n<b>Описание</b>: {product['description']}\n<b>Марка</b>: {product['brand']}\n<b>Модель</b>: {product['product_model']}\n<b>Комплектация</b>: {product['equipment']}\n<b>Производитель</b>: {product['manufacturer']}\n<b>Год выпуска</b>: {product['year']}\n<b>Стоимость</b>: {price} {product['currency']}\n<b>Статус</b>: {product['status']}"
                filtered_lines = [line for line in s.split('\n') if line.split(':')[1] not in (' None', ' ')]
                result = '\n'.join(filtered_lines)
                a = await bot.send_message(callback_query.from_user.id, text=result.replace('None', '')+promotion, reply_markup=get_product_kb(media, products, kp), parse_mode=types.ParseMode.HTML)
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=current_data['product_message_id'])
                current_data['product_message_id'] = a.message_id

            current_data['product_name'] = product['name']
            current_data['product_price'] = product['price']
            # else:
            #     print(current_data['product_name'], product['name'], str(current_data['product_price']), str(product['price']), sep='\n')
            #     await callback_query.answer("Достигнут край списка продуктов.", show_alert=True)

        except Exception as e:
            if current_index == len(products):
                current_data['current_index'] = 0
                product = products[0]
            else:
                current_data['current_index'] = len(products)-1
                product = products[len(products)-1]
            await create_product_views(product["id"])
            photo = await download_photo(product["photo"])
            #if current_data['product_name'] != product['name'] and str(current_data['product_price']) != str(product['price']):
            promotion = '\n\nАкция!' if product['promotion'] else ''
            price = '{:,.0f}'.format(float(product['price'])).replace(',', ' ')
            media = await get_product_media(str(product['id']))
            kp = await get_kp_path(product['id'])
            if photo:
                s = f"<b>ID товара</b>: {product['id']}\n<b>Название</b>: {product['name']}\n<b>Описание</b>: {product['description']}\n<b>Марка</b>: {product['brand']}\n<b>Модель</b>: {product['product_model']}\n<b>Комплектация</b>: {product['equipment']}\n<b>Производитель</b>: {product['manufacturer']}\n<b>Год выпуска</b>: {product['year']}\n<b>Стоимость</b>: {price} {product['currency']}\n<b>Статус</b>: {product['status']}"
                filtered_lines = [line for line in s.split('\n') if line.split(':')[1] not in (' None', ' ')]
                result = '\n'.join(filtered_lines)
                a = await bot.send_photo(callback_query.from_user.id, photo, caption=result.replace('None', '')+promotion, reply_markup=get_product_kb(media, products, kp), parse_mode=types.ParseMode.HTML)
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=current_data['product_message_id'])
                current_data['product_message_id'] = a.message_id
            else:
                s = f"<b>ID товара</b>: {product['id']}\n<b>Название</b>: {product['name']}\n<b>Описание</b>: {product['description']}\n<b>Марка</b>: {product['brand']}\n<b>Модель</b>: {product['product_model']}\n<b>Комплектация</b>: {product['equipment']}\n<b>Производитель</b>: {product['manufacturer']}\n<b>Год выпуска</b>: {product['year']}\n<b>Стоимость</b>: {price} {product['currency']}\n<b>Статус</b>: {product['status']}"
                filtered_lines = [line for line in s.split('\n') if line.split(':')[1] not in (' None', ' ')]
                result = '\n'.join(filtered_lines)
                a = await bot.send_message(callback_query.from_user.id, text=result.replace('None', '')+promotion, reply_markup=get_product_kb(media, products, kp), parse_mode=types.ParseMode.HTML)
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=current_data['product_message_id'])
                current_data['product_message_id'] = a.message_id

            current_data['product_name'] = product['name']
            current_data['product_price'] = product['price']
            # else:
            #     await callback_query.answer("Достигнут край списка продуктов.", show_alert=True)



@dp.callback_query_handler(lambda query: True, state=SearchStatesGroup.year)
async def process_brand(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(selected_year=callback_query.data)
    async with state.proxy() as data:
        selected_species = data.get("selected_species")
        selected_wheels = data.get("selected_wheels")
        selected_brand = data.get("selected_brand")
        selected_country = data.get("selected_country")
        selected_year = data.get("selected_year")
        data_list = data.get("data_list")

        filters = [selected_country, selected_wheels, selected_brand, selected_species, selected_year]

        filtered_data_list = []
        for d in data_list:
            if (d['brand'] == filters[2] and
                str(d['year']) == filters[-1] and
                d['manufacturer'] == filters[3] and
                d['species'] == filters[0] and
                d['wheels'] == filters[1]):
                filtered_data_list.append(d)



        if filtered_data_list:
            # Сохраняем список продуктов и текущий индекс элемента в FSM
            async with state.proxy() as data:
                data['products'] = filtered_data_list
                data['current_index'] = 0
 
                product = filtered_data_list[0]
                await create_product_views(product["id"])



                photo = await download_photo(product["photo"])
                promotion = '\n\nАкция!' if product['promotion'] else ''
                if product['price'] != None:
                    price = '{:,.0f}'.format(float(product['price'])).replace(',', ' ')
                media = await get_product_media(str(product['id']))
                kp = await get_kp_path(product['id'])
                if photo!=None:
                    s = f"<b>ID товара</b>: {product['id']}\n<b>Название</b>: {product['name']}\n<b>Описание</b>: {product['description']}\n<b>Марка</b>: {product['brand']}\n<b>Модель</b>: {product['product_model']}\n<b>Комплектация</b>: {product['equipment']}\n<b>Производитель</b>: {product['manufacturer']}\n<b>Год выпуска</b>: {product['year']}\n<b>Стоимость</b>: {price} {product['currency']}\n<b>Статус</b>: {product['status']}"
                    filtered_lines = [line for line in s.split('\n') if line.split(':')[1] not in (' None', ' ')]
                    result = '\n'.join(filtered_lines)
                    a = await bot.send_photo(callback_query.from_user.id, photo, caption=result.replace('None', '')+promotion, reply_markup=get_product_kb(media,filtered_data_list, kp), parse_mode=types.ParseMode.HTML)
                    data['product_message_id'] = a.message_id
                    data['product_name'] = product['name']
                    data['product_price'] = product['price']
                else:
                    s = f"<b>ID товара</b>: {product['id']}\n<b>Название</b>: {product['name']}\n<b>Описание</b>: {product['description']}\n<b>Марка</b>: {product['brand']}\n<b>Модель</b>: {product['product_model']}\n<b>Комплектация</b>: {product['equipment']}\n<b>Производитель</b>: {product['manufacturer']}\n<b>Год выпуска</b>: {product['year']}\n<b>Стоимость</b>: {price} {product['currency']}\n<b>Статус</b>: {product['status']}"
                    filtered_lines = [line for line in s.split('\n') if line.split(':')[1] not in (' None', ' ')]
                    result = '\n'.join(filtered_lines)
                    a = await bot.send_message(callback_query.from_user.id, text=result.replace('None', '')+promotion, reply_markup=get_product_kb(media, filtered_data_list, kp), parse_mode=types.ParseMode.HTML)
                    data['product_message_id'] = a.message_id
                    data['product_name'] = product['name']
                    data['product_price'] = product['price']
        else:

            await bot.send_message(callback_query.from_user.id, text="Список продуктов пуст.", reply_markup=get_menu_keyboard())






@dp.callback_query_handler(lambda query: True)
async def callback_category(callback_query: CallbackQuery, state: FSMContext):
    parent_id = callback_query.data
    data = await state.get_data()
    new_categories = []

    if not data.get('CATEGORIES'):
        data['ALL_CATEGORIES'] = await get_categories_list()
        data['CATEGORIES'] = data['ALL_CATEGORIES'][:]

    CATEGORIES = data['CATEGORIES']
    child = [i['name'] for i in CATEGORIES if str(i['id']) == str(parent_id)][0]
    new_categories = await find_children(CATEGORIES, child)
    child_id = [i["id"] for i in data['CATEGORIES'] if i["name"] == child][0]

    if type(new_categories)==list and len(new_categories):
        data['CATEGORIES'] = new_categories
    else:
        #a = await bot.send_message(callback_query.from_user.id, "OK", reply_markup=ReplyKeyboardRemove())
        #await bot.delete_message(callback_query.from_user.id, a.message_id)
        category_id = int(new_categories)
        logging.info(f"Телеграм-пользователь {callback_query.from_user.username} просматривает товары категории {category_id}")
        a = await create_category_views(str(category_id))
        # b = await increment_category_views(str(category_id))
        data_list = await get_products_list(category_id=category_id)

        if data_list:
            # Сохраняем список продуктов и текущий индекс элемента в FSM
            async with state.proxy() as data:
                data['products'] = data_list
                data['current_index'] = 0

                product = data_list[0]
                await create_product_views(product["id"])



                photo = await download_photo(product["photo"])
                promotion = '\n\nАкция!' if product['promotion'] else ''
                price = '{:,.0f}'.format(float(product['price'])).replace(',', ' ')
                media = await get_product_media(str(product['id']))
                kp = await get_kp_path(product['id'])
                if photo!=None:
                    s = f"<b>ID товара</b>: {product['id']}\n<b>Название</b>: {product['name']}\n<b>Описание</b>: {product['description']}\n<b>Марка</b>: {product['brand']}\n<b>Модель</b>: {product['product_model']}\n<b>Комплектация</b>: {product['equipment']}\n<b>Производитель</b>: {product['manufacturer']}\n<b>Год выпуска</b>: {product['year']}\n<b>Стоимость</b>: {price} {product['currency']}\n<b>Статус</b>: {product['status']}"
                    filtered_lines = [line for line in s.split('\n') if line.split(':')[1] not in (' None', ' ')]
                    result = '\n'.join(filtered_lines)
                    a = await bot.send_photo(callback_query.from_user.id, photo, caption=result.replace('None', ' ')+promotion, reply_markup=get_product_kb(media, data_list, kp), parse_mode=types.ParseMode.HTML)
                    data['product_message_id'] = a.message_id
                    data['product_name'] = product['name']
                    data['product_price'] = product['price']
                else:
                    s = f"<b>ID товара</b>: {product['id']}\n<b>Название</b>: {product['name']}\n<b>Описание</b>: {product['description']}\n<b>Марка</b>: {product['brand']}\n<b>Модель</b>: {product['product_model']}\n<b>Комплектация</b>: {product['equipment']}\n<b>Производитель</b>: {product['manufacturer']}\n<b>Год выпуска</b>: {product['year']}\n<b>Стоимость</b>: {price} {product['currency']}\n<b>Статус</b>: {product['status']}"
                    filtered_lines = [line for line in s.split('\n') if line.split(':')[1] not in (' None', ' ')]
                    result = '\n'.join(filtered_lines)
                    a = await bot.send_message(callback_query.from_user.id, text=result.replace('None', ' ')+promotion, reply_markup=get_product_kb(media, data_list, kp), parse_mode=types.ParseMode.HTML)
                    data['product_message_id'] = a.message_id
                    data['product_name'] = product['name']
                    data['product_price'] = product['price']
                # caption = result.replace('None', '')+promotion
                # photo_pathes = await get_product_media(product['id']) # list with pathes
                # media_group = [InputMediaPhoto(media=types.InputFile(rf'{path}')) if path!=photo_pathes[-1] else InputMediaPhoto(media=types.InputFile(rf'{path}'), caption=caption) for path in photo_pathes]
                # try:
                #     b = await bot.send_media_group(callback_query.from_user.id, media=media_group)

                # except:
                #     b = await bot.send_message(callback_query.from_user.id, caption)

        else:

            await bot.send_message(callback_query.from_user.id, text="Список продуктов пуст.")

    # await ProductState.current_index.set()

    await state.set_data(data)

    message_id = data['message_id']

    try:
        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=message_id, reply_markup=create_category_keyboard_with_menu([i for i in new_categories if i['parent'] == child_id]))
        # else:
        #     await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=message_id, reply_markup=create_category_keyboard(['Результаты']))
    except:
        None




if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)




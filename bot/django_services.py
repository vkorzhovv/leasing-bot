from bot.bot import storage, bot, dp, TOKEN, admin_id, admin_password, admin_username, domen
from faker import Faker
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
import aiohttp
import requests
from asgiref.sync import sync_to_async
import asyncio


async def download_photo(img_url):
    try:
        auth = aiohttp.BasicAuth(admin_username, admin_password)

        async with aiohttp.ClientSession(auth=auth) as session:
            async with session.get(img_url) as response:
                photo_bytes = await response.read()
                return photo_bytes
    except:
        return None


def set_manager_kb():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Подтвердить', callback_data="manager")
    keyboard.row(button1)
    return keyboard

async def register_manager(CHAT_ID: str):
    fake = Faker()

    username = fake.user_name()
    password = fake.password()

    await bot.send_message(CHAT_ID, f'username: {username}\npassword: {password}\nadmin-panel: {domen}', reply_markup=set_manager_kb())


async def download_photo(img_url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(img_url) as response:
                photo_bytes = await response.read()
                return photo_bytes
    except:
        return None


#POSTS -----------------------------------------------------------------------------

def set_post_kb():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Подтвердить', callback_data="post")
    button2 = InlineKeyboardButton('Отклонить', callback_data="no_post")
    keyboard.row(button1)
    keyboard.row(button2)
    return keyboard

async def get_post_path(post_id):
    url = f'{domen}api/get_media_urls/{post_id}/'
    auth = aiohttp.BasicAuth(admin_username, admin_password)

    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(url) as response:
            if response.status == 200:
                data_list = await response.json()
                return data_list
            else:
                return None


async def send_post(post, media_paths=None):


    message = post.split('\n')



    user_id = admin_id

    post_id = message[0].split(': ')[1]


    media = []


    #media_paths = await get_post_path(post_id)


    if media_paths:
        for photo_path in media_paths:
            if photo_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                media_type = types.InputMediaPhoto
            elif photo_path.lower().endswith(('.mp4', '.avi', '.mkv')):
                media_type = types.InputMediaVideo
            else:
                continue
            photo_file = open(photo_path, 'rb')
            input_media = media_type(media=types.InputFile(photo_file))
            media.append(input_media)

        await bot.send_media_group(chat_id=user_id, media=media)
        await bot.send_message(user_id, post, reply_markup=set_post_kb())

        photo_file.close()
    else:
        await bot.send_message(user_id, post, reply_markup=set_post_kb())



#POLLS -----------------------------------------------------------------------------

def set_options_kb(options):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(o[1], callback_data=f'option_{o[0]}') for o in options]
    keyboard.add(*buttons)

    return keyboard

def set_poll_kb():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Подтвердить', callback_data="poll")
    button2 = InlineKeyboardButton('Отклонить', callback_data="no_poll")
    keyboard.row(button1)
    keyboard.row(button2)
    return keyboard


async def get_poll_path(poll_id):
    url = f'{domen}api/get_poll_media_urls/{poll_id}/'
    auth = aiohttp.BasicAuth(admin_username, admin_password)

    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(url) as response:
            if response.status == 200:
                data_list = await response.json()
                return data_list
            else:
                return None



async def send_poll(poll_id, options, title, time, media_paths=None):
    if media_paths != []:
        media = types.MediaGroup()
        for path in media_paths:
            media.attach_photo(types.InputFile(rf'{path}'))

        await bot.send_media_group(admin_id, media=media)
    await bot.send_message(admin_id, f'{title}', reply_markup=set_options_kb(options))
    if time!=None:
        await bot.send_message(admin_id, f'Опрос: {poll_id}\nЗапланирован на: {time}', reply_markup=set_poll_kb())
    else:
        await bot.send_message(admin_id, f'Опрос: {poll_id}', reply_markup=set_poll_kb())

# async def send_poll(poll, media_paths=None):
#     media = []

#     user_id = admin_id

#     message = poll.split('\n')

#     poll_id = message[0]
#     options = message[2].split(': ')[1].split(',')
#     title = message[1]
#     correct_option = message[3].split(': ')[1]
#     manager_id = message[-1]

#     #media_paths = await get_poll_path(poll_id)
#     poll_options = [types.PollOption(text=i, voter_count=0) for i in options]

#     if media_paths:
#         for photo_path in media_paths:
#             if photo_path.lower().endswith(('.jpg', '.jpeg', '.png')):
#                 media_type = types.InputMediaPhoto
#             elif photo_path.lower().endswith(('.mp4', '.avi', '.mkv')):
#                 media_type = types.InputMediaVideo
#             else:
#                 continue
#             photo_file = open(photo_path, 'rb')
#             input_media = media_type(media=types.InputFile(photo_file))
#             media.append(input_media)



#         if correct_option is not None and correct_option.isdigit():

#             poll = types.Poll(question=title,
#                             options=[o.text for o in poll_options],
#                             type=types.PollType.QUIZ,
#                             correct_option_id=int(correct_option)-1)

#             await bot.send_media_group(chat_id=user_id, media=media)
#             await bot.send_poll(chat_id=user_id,
#                                 question=poll.question,
#                                 options=[o.text for o in poll_options],
#                                 type=poll.type,
#                                 correct_option_id=poll.correct_option_id)
#             await bot.send_message(user_id, f'{poll_id}\n{title}\n{message[2]}\n{message[3]}\n{message[4]}\n{manager_id}', reply_markup=set_poll_kb())
#         else:
#             poll = types.Poll(question=title,
#                             options=[o.text for o in poll_options],
#                             type=types.PollType.REGULAR,
#                             )

#             await bot.send_media_group(chat_id=user_id, media=media)
#             await bot.send_poll(chat_id=user_id,
#                                 question=poll.question,
#                                 options=[o.text for o in poll_options],
#                                 type=poll.type,
#                                 )
#             await bot.send_message(user_id, f'{poll_id}\n{title}\n{message[2]}\n{message[3]}\n{message[4]}\n{manager_id}', reply_markup=set_poll_kb())


#     else:
#         if correct_option is not None and correct_option.isdigit():

#             poll = types.Poll(question=title,
#                             options=[o.text for o in poll_options],
#                             type=types.PollType.QUIZ,
#                             correct_option_id=int(correct_option)-1)

#             await bot.send_poll(chat_id=user_id,
#                                 question=poll.question,
#                                 options=[o.text for o in poll_options],
#                                 type=poll.type,
#                                 correct_option_id=poll.correct_option_id)
#             await bot.send_message(user_id, f'{poll_id}\n{title}\n{message[2]}\n{message[3]}\n{message[4]}\n{manager_id}', reply_markup=set_poll_kb())
#         else:
#             poll = types.Poll(question=title,
#                             options=[o.text for o in poll_options],
#                             type=types.PollType.REGULAR,
#                             )

#             await bot.send_poll(chat_id=user_id,
#                                 question=poll.question,
#                                 options=[o.text for o in poll_options],
#                                 type=poll.type,
#                                 )
#             await bot.send_message(user_id, f'{poll_id}\n{title}\n{message[2]}\n{message[3]}\n{message[4]}\n{manager_id}', reply_markup=set_poll_kb())




# stories news for admin approve

def approve_storynews_kb():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Подтвердить', callback_data="storynews")
    button2 = InlineKeyboardButton('Отклонить', callback_data="no_storynews")
    keyboard.row(button1)
    keyboard.row(button2)
    return keyboard

async def send_storynews_admin(storynews, manager):
    try:
        photo = storynews.photo.path
        await bot.send_photo(admin_id, open(photo, 'rb'), caption=f"ID актуального/новости: {storynews.id}\nНовость или актуальное: {storynews.get_sort_display()}\nНазвание: {storynews.name}\nОписание: {storynews.description}\nТелеграм-ID менеджера: {manager} ({storynews.user.extended_user.user.username})", reply_markup=approve_storynews_kb())
    except:
        await bot.send_message(admin_id, f"ID актуального/новости: {storynews.id}\nНовость или актуальное: {storynews.get_sort_display()}\nНазвание: {storynews.name}\nОписание: {storynews.description}\nТелеграм-ID менеджера: {manager} ({storynews.user.extended_user.user.username})", reply_markup=approve_storynews_kb())

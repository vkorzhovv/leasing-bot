import aiohttp
import aiogram
import asyncio
import json
import requests
from faker import Faker
from aiogram import Bot,types
from bot import storage, bot, dp, TOKEN, admin_username, admin_password, domen, admin_tg, admin_id
import datetime
from dateutil.parser import parse
import datetime
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import logging
import random


def set_options_kb(options):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(o[1], callback_data=f'option_{o[0]}') for o in options]
    keyboard.add(*buttons)

    return keyboard


# Внесение зарегистрированного пользователя в БД
async def create_bot_user(name, company_name, city, phone, user_id, username):

    url = f"{domen}api/create_bot_user/"

    data = {
            "name": name,
            "company_name": company_name,
            "city": city,
            "phone": phone,
            "user_id": user_id,
            "username": username
        }

    auth = aiohttp.BasicAuth(admin_username, admin_password)

    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.post(url, json=data) as response:
            if response.status == 201:
                return await response.json()
            else:
                error_message = await response.text()
                print(f"Error: {response.status} - {error_message}")
                return None


# Получение текста для команд по ключам
async def get_commands_list():
    url = f"{domen}api/commands/"
    auth = aiohttp.BasicAuth(admin_username, admin_password)

    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(url) as response:
            try:
                response_data = await response.json()
                if response.status == 200:
                    merged_dict = {key: value for item in response_data for key, value in item.items()}
                    return merged_dict
                else:
                    return []
            except: # Вывести информацию об исключении для отладки
                return []


# Отправка фотографии с текстом во время регистрации
async def send_photo_with_url(TOKEN, CHAT_ID, img_url, caption, parse_mode = 'HTML', message=None):
    if '<p>' in caption:
        caption = caption[3:-4]
    if img_url!=None:
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

        auth = aiohttp.BasicAuth(admin_username, admin_password)

        async with aiohttp.ClientSession(auth=auth) as session:
            async with session.get(img_url) as response:
                photo_bytes = await response.read()

        # Отправляем фото на Telegram с использованием параметра 'chat_id' в 'params'
        async with aiohttp.ClientSession(auth=auth) as session:
            async with session.post(url, params={"chat_id": CHAT_ID, "caption":caption, "parse_mode":parse_mode}, data={"photo": photo_bytes}) as response:
                print(response.status)
    else:
        try:
            await message.reply(caption, parse_mode=types.ParseMode.HTML)
        except:
            await bot.send_message(CHAT_ID, caption, parse_mode=types.ParseMode.HTML)

async def send_photo_with_keyboard(TOKEN, CHAT_ID, img_url, caption, keyboard_data, message=None):
    if img_url is not None:
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

        auth = aiohttp.BasicAuth(admin_username, admin_password)

        async with aiohttp.ClientSession(auth=auth) as session:
            async with session.get(img_url) as response:
                photo_bytes = await response.read()

        # Отправляем фото на Telegram с использованием параметров 'chat_id', 'caption' и 'reply_markup'
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params={"chat_id": CHAT_ID, "caption": caption}, data={"photo": photo_bytes, "reply_markup": keyboard_data}) as response:
                print(response.status)
    else:
        await message.reply(caption)




# Получаем список категорий
async def get_categories_list():
    url = f"{domen}api/categories/"

    auth = aiohttp.BasicAuth(admin_username, admin_password)

    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(url) as response:
            if response.status == 200:
                data_list = await response.json()
                data_list = list(sorted(data_list, key=lambda x: x['position']if x['position']!=None else 1000))
                return data_list
            else:
                return None


# Получаем всех потомков указанной категории
async def find_children(lst, parent_name):
    parent_ids = [item["id"] for item in lst if item["name"] == parent_name]
    result = []

    async def find_recursive(parent_ids, ancestors=[]):
        children = [item for item in lst if item["parent"] in parent_ids]
        if not children:
            return

        result.extend(children)
        new_parent_ids = [item["id"] for item in children]
        new_ancestors = ancestors + parent_ids
        await find_recursive(new_parent_ids, new_ancestors)

    await find_recursive(parent_ids)

    if not result:
        return parent_ids[0]
    return result


# Проверка на потомков корневой категории ("Каталог") для добавления в их клавиатуру кнопки "Меню" (она есть только у них)
async def check_categories(ALL_CATEGORIES, CATEGORIES):
    for i in ALL_CATEGORIES:
        if i['id'] == CATEGORIES[0]["parent"] and i['name'] == 'Каталог':
            return True
    return False


# Сохдание команды
async def create_command(key, text):
    url = f"{domen}api/create_command/"

    data = {
            "key": key,
            "description": "команда была создана автоматически",
            "text": f"<p>{text}</p>",
        }


    auth = aiohttp.BasicAuth(admin_username, admin_password)

    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.post(url, json=data) as response:
            if response.status == 201:
                return await response.json()
            else:
                error_message = await response.text()
                print(f"Error: {response.status} - {error_message}")
                return None


async def get_products_list(category_id):
    url = f"{domen}api/products/"

    params = {'category_id': category_id}

    auth = aiohttp.BasicAuth(admin_username, admin_password)

    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data_list = await response.json()
                data_list = list(sorted(data_list, key=lambda x: x['position']if x['position']!=None else 1000))
                return data_list
            else:
                return None


async def activate_user(user_id):
    url = f"{domen}api/activate/{user_id}/"
    headers = {'Content-Type': 'application/json'}
    data = {'activated': True}

    auth = aiohttp.BasicAuth(admin_username, admin_password)

    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.put(url, headers=headers, json=data) as response:
            if response.status == 200:
                print(f"User with user_id={user_id} has been activated successfully.")
            elif response.status == 404:
                print(f"User with user_id={user_id} not found.")
            else:
                print(f"Failed to activate user with user_id={user_id}. Status code: {response.status}")


async def download_photo(img_url):
    try:
        auth = aiohttp.BasicAuth(admin_username, admin_password)

        async with aiohttp.ClientSession(auth=auth) as session:
            async with session.get(img_url) as response:
                photo_bytes = await response.read()
                return photo_bytes
    except:
        return None


async def get_news_or_stories_list(stories_or_news):
    url = f"{domen}api/{stories_or_news}/"

    auth = aiohttp.BasicAuth(admin_username, admin_password)

    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(url) as response:
            if response.status == 200:
                data_list = await response.json()
                data_list = list(sorted(data_list, key=lambda x: x['position']if x['position']!=None else 1000))
                return data_list
            else:
                return None


async def get_promotions_list():
    url = f"{domen}api/promotion_products/"

    auth = aiohttp.BasicAuth(admin_username, admin_password)

    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(url) as response:
            if response.status == 200:
                data_list = await response.json()
                return data_list
            else:
                return None


async def send_last_interaction(user_id):
    url = f'{domen}api/update_last_interaction/'
    data = {'user_id': user_id}

    auth = aiohttp.BasicAuth(admin_username, admin_password)

    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                response_json = await response.json()
            else:
                response_text = await response.text()


# async def register_manager(CHAT_ID: str):
#     fake = Faker()

#     username = fake.user_name()
#     password = fake.password()

#     await bot.send_message(CHAT_ID, f'username: {username}\npassword: {password}\nadmin-panel: http://localhost:8000/admin', reply_markup=set_manager_kb())



async def save_manager(username, password, bot_user_id):
    url = f'{domen}api/register/'

    data = {
        "username": username,
        "password": password,
        "bot_user_id": bot_user_id
    }

    auth = aiohttp.BasicAuth(admin_username, admin_password)

    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.post(url, json=data) as response:
            if response.status == 201:
                response_data = await response.json()
                return [username, password]

            else:
                response_text = await response.text()


async def get_botusers(group_id=None):
    url = f'{domen}api/list_bot_user/'

    if group_id is not None:
        url += f'?group_id={group_id}'

    auth = aiohttp.BasicAuth(admin_username, admin_password)

    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(url) as response:
            if response.status == 200:
                data_list = await response.json()
                return [i['user_id'] for i in data_list]
            else:
                return None

async def change_post_status(post_id):
    url = f'{domen}api/approve_post/{post_id}/'

    auth = aiohttp.BasicAuth(admin_username, admin_password)

    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.patch(url, json={"post_id": post_id}) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None


async def do_mailing(post):
    try:
        if post[2].split(': ')[1].isdigit():
            users = await get_botusers(post[2].split(': ')[1])
            await post_post_users_count(post[0].split(': ')[1], len(users))
        else:
            users = await get_botusers()
            await post_post_users_count(post[0].split(': ')[1], len(users))
    except:
        users = await get_botusers()
        await post_post_users_count(post[0].split(': ')[1], len(users))
    for user in users:
        try:
            await send_post(user, post)
        except:
            None


async def schedule_mailing(message, time):

    dt_object = parse(time)
    dt_utc = dt_object.astimezone(datetime.timezone.utc)
    t = dt_utc

    # Текущее время, осведомленное о смещении
    now = datetime.datetime.now(datetime.timezone.utc)

    # Вычисляем время до заданного времени
    time_difference = (t - now).total_seconds()

    # Ожидаем до заданного времени
    await asyncio.sleep(time_difference)

    # Вызываем асинхронную функцию для рассылки
    await do_mailing(message)


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


async def send_post(user_id, message):

    post_id = message[0].split(': ')[1]



    media = []

    media_paths = await get_post_path(post_id)

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


        media[0]["caption"] = message[1].split(': ')[1]

        await bot.send_media_group(chat_id=user_id, media=media)
        photo_file.close()
    else:
        await bot.send_message(user_id, message[1].split(': ')[1])




# POLLS
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


async def change_poll_status(poll_id):
    url = f'{domen}api/approve_poll/{poll_id}/'

    auth = aiohttp.BasicAuth(admin_username, admin_password)

    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.patch(url, json={"poll_id": poll_id}) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None


async def do_poll_mailing(poll_id, options, title, poll_group=None, media_paths=None):
    #poll_id = poll[0].split(': ')[1]

    if poll_group:
        users = await get_botusers(poll_group)
        if users:
            await post_poll_users_count(poll_id=poll_id, users_count=len(users))
    else:
        users = await get_botusers()
        if users:
            await post_poll_users_count(poll_id=poll_id, users_count=len(users))
    # except:
    #     users = await get_botusers()
    #     await post_poll_users_count(poll_id=poll_id, users_count=len(users))
    print(users)
    for user in users:
        try:
            await send_poll(user, options, title, media_paths)
        except:
            None


async def schedule_poll_mailing(poll_id, options, title, time, poll_group=None, media_paths=None):

    dt_object = parse(time)
    dt_utc = dt_object.astimezone(datetime.timezone.utc)
    t = dt_utc

    # Текущее время, осведомленное о смещении
    now = datetime.datetime.now(datetime.timezone.utc)

    # Вычисляем время до заданного времени
    time_difference = (t - now).total_seconds()

    # Ожидаем до заданного времени
    await asyncio.sleep(time_difference)

    # Вызываем асинхронную функцию для рассылки
    await do_poll_mailing(poll_id, options, title, poll_group, media_paths)



async def send_poll(user, options, title, media_paths=None):
    if media_paths != []:
        media = types.MediaGroup()
        for path in media_paths:
            media.attach_photo(types.InputFile(rf'{path}'))

        await bot.send_media_group(user, media=media)
    await bot.send_message(user, f'{title}', reply_markup=set_options_kb(options))

# async def send_poll(user_id, message):
    # media = []

    # poll_id = message[0].split(': ')[1]
    # options = message[2].split(': ')[1].split(',')
    # title = message[1].split(': ')[1]
    # correct_option = message[3].split(': ')[1]

    # media_paths = await get_poll_path(poll_id)

    # poll_options = [types.PollOption(text=i, voter_count=0) for i in options]

    # if len(media_paths)>0:
    #     for photo_path in media_paths:
    #         if photo_path.lower().endswith(('.jpg', '.jpeg', '.png')):
    #             media_type = types.InputMediaPhoto
    #         elif photo_path.lower().endswith(('.mp4', '.avi', '.mkv')):
    #             media_type = types.InputMediaVideo
    #         else:
    #             continue
    #         photo_file = open(photo_path, 'rb')
    #         input_media = media_type(media=types.InputFile(photo_file))
    #         media.append(input_media)




    #     if correct_option is not None and correct_option.isdigit():
    #         poll = types.Poll(question=title,
    #                         options=[o.text for o in poll_options],
    #                         type=types.PollType.QUIZ,
    #                         correct_option_id=int(correct_option)-1)

    #         await bot.send_media_group(chat_id=user_id, media=media)
    #         await bot.send_poll(chat_id=user_id,
    #                             question=poll.question,
    #                             options=[o.text for o in poll_options],
    #                             type=poll.type,
    #                             correct_option_id=poll.correct_option_id)
    #     else:
    #         poll = types.Poll(question=title,
    #                         options=[o.text for o in poll_options],
    #                         type=types.PollType.REGULAR,
    #                         )

    #         await bot.send_media_group(chat_id=user_id, media=media)
    #         await bot.send_poll(chat_id=user_id,
    #                             question=poll.question,
    #                             options=[o.text for o in poll_options],
    #                             type=poll.type,
    #                             )
    # else:
    #     if correct_option is not None and correct_option.isdigit():
    #         poll = types.Poll(question=title,
    #                         options=[o.text for o in poll_options],
    #                         type=types.PollType.QUIZ,
    #                         correct_option_id=int(correct_option)-1)

    #         await bot.send_poll(chat_id=user_id,
    #                             question=poll.question,
    #                             options=[o.text for o in poll_options],
    #                             type=poll.type,
    #                             correct_option_id=poll.correct_option_id)
    #     else:
    #         poll = types.Poll(question=title,
    #                                 options=[o.text for o in poll_options],
    #                                 type=types.PollType.REGULAR,
    #                                 )

    #         await bot.send_poll(chat_id=user_id,
    #                             question=poll.question,
    #                             options=[o.text for o in poll_options],
    #                             type=poll.type,
    #                             )




#storynews change approved
async def change_storynews_status(post_id):
    url = f'{domen}api/approve/{post_id}/'

    auth = aiohttp.BasicAuth(admin_username, admin_password)

    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.patch(url, json={"storynews_id": post_id}) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None


async def check_botuser_exists(user_id):
    url = f'{domen}api/check_bot_user_exists/'
    data = {'user_id': user_id}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result['user_id']  # Вернуть True или False в зависимости от ответа
            else:
                # Обработка ошибки, если что-то пошло не так
                return None


async def check_botuser_activated(user_id):
    url = f'{domen}api/check_bot_user_activated/'
    data = {'user_id': user_id}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result['user_id']  # Вернуть True или False в зависимости от ответа
            else:
                # Обработка ошибки, если что-то пошло не так
                return None


async def post_poll_users_count(poll_id, users_count):
    url = f"{domen}api/create_poll_users_count/"  # Замените на ваш реальный URL

    data = {
        'poll': poll_id,
        'users_count': users_count
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            if response.status == 201:
                print("PollUsersCount created successfully!")
            else:
                print("Error creating PollUsersCount:", response.status)


async def post_post_users_count(post_id, users_count):
    url = f"{domen}api/create_post_users_count/"  # Замените на ваш реальный URL

    data = {
        'post': post_id,
        'users_count': users_count
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            if response.status == 201:
                print("PostUsersCount created successfully!")
            else:
                print("Error creating PostUsersCount:", response.status)


async def create_storynews_views(item_id):
    url = f"{domen}api/create_storynews_views/"

    data = {
        "item": item_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            response_data = await response.json()
            return response_data



async def increment_story_views(item_id):
    url = f"{domen}api/increment_story_views/"  # Замените на ваш реальный URL

    data = {
        "item_id": item_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            if response.status == 200:
                response_data = await response.json()
                return response_data
            else:
                return None


async def increment_product_views(product_id):
    url = f"{domen}api/increment_products_views/"  # Замените на ваш реальный URL

    data = {
        "product_id": product_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            if response.status == 200:
                response_data = await response.json()
                return response_data
            else:
                return None


async def create_product_views(product_id):
    url = f"{domen}api/create_product_views/"

    data = {
        "product": product_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            response_data = await response.json()
            return response_data

async def create_product_kp(product_id):
    url = f"{domen}api/create_product_kp/"

    data = {
        "product": product_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            response_data = await response.json()
            return response_data


async def create_product_chat(product_id):
    url = f"{domen}api/create_product_chat/"

    data = {
        "product": product_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            response_data = await response.json()
            return response_data



async def increment_category_views(category_id):
    url = f"{domen}api/increment_category_views/"  # Замените на ваш реальный URL

    data = {
        "category_id": category_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            if response.status == 200:
                response_data = await response.json()
                return response_data
            else:
                return None


async def create_category_views(category_id):
    url = f"{domen}api/create_category_views/"

    data = {
        "category": category_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            response_data = await response.json()
            return response_data



async def get_manager_with_category(product_id):
    endpoint = f"{domen}api/users_with_category/{product_id}/"

    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint) as response:
            if response.status == 200:
                data = await response.json()
                if data:
                    return data#[0]['telegram_username']
                else:
                    return admin_tg
            else:
                return "Error fetching data"




async def get_city_from_location(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            city = data.get("address", {}).get("city", "Unknown City")
            return city


async def update_botuser_city(user_id, new_city):
    auth = aiohttp.BasicAuth(admin_username, admin_password)
    async with aiohttp.ClientSession(auth=auth) as session:
        url = f'{domen}api/botusers/{user_id}/update_city/'

        async with session.patch(url, json={"city": new_city}) as response:
            if response.status == 200:  # Check if the response is successful
                try:
                    response_json = await response.json()
                    return response_json
                except aiohttp.client_exceptions.ContentTypeError:
                    # Handle the unexpected content type error
                    return {'error': 'Unexpected content type in response'}
            else:
                return {'error': f'Server returned status {response.status}'}


async def create_manager_request(product, manager, bot_user):
    url = f"{domen}api/create_manager_request/"  # Замените на фактический URL
    data = {
        "product": product,
        "manager": manager,
        "bot_user": bot_user
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 201:  # Ожидаемый статус создания объекта
                result = await response.json()
                print("Manager request created:", result)
            else:
                print("Error creating manager request:", response.status)



async def search_manager_id(manager_username):
    url = f"{domen}api/bot_user/search/{manager_username}/"  # Замените на фактический URL


    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 201:  # Ожидаемый статус создания объекта
                result = await response.json()
                return result
            else:
                result = await response.json()
                return result


async def search_user_by_id(user_id):
    url = f"{domen}api/bot_user_id/search/{user_id}/"  # Замените на фактический URL


    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 201:  # Ожидаемый статус создания объекта
                result = await response.json()
                return result
            else:
                result = await response.json()
                return result



async def get_product_media(product_id):
    url = f'{domen}api/product_media/{product_id}/'  # Замените на реальный URL

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return [i['absolute_media_path'] for i in data]
            else:
                print(f'Error fetching data. Status code: {response.status}')
                return None


async def get_kp_path(product_id):
    url = f'{domen}api/get_kp_path/{product_id}/'  # Замените на свой URL

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                kp_path = data.get('kp_path')
                return kp_path
            else:
                return None


async def create_kp_request(product, manager, bot_user):
    url = f"{domen}api/create_kp_request/"  # Замените на фактический URL
    data = {
        "product": product,
        "manager": manager,
        "bot_user": bot_user
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 201:  # Ожидаемый статус создания объекта
                result = await response.json()
                print("Manager request created:", result)
            else:
                print("Error creating manager request:", response.status)


async def increment_product_kp(product_id):
    url = f"{domen}api/increment_products_kp/"  # Замените на ваш реальный URL

    data = {
        "product_id": product_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            if response.status == 200:
                response_data = await response.json()
                return response_data
            else:
                return None

async def increment_product_manager_chat(product_id):
    url = f"{domen}api/increment_products_manager_chat/"  # Замените на ваш реальный URL

    data = {
        "product_id": product_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            if response.status == 200:
                response_data = await response.json()
                return response_data
            else:
                return None


async def fetch_poll_option(option_id):
    url = f'{domen}api/get_poll_option/{option_id}/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def fetch_poll(poll_id):
    url = f'{domen}api/get_poll/{poll_id}/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                return await response.json()
            except:
                print('Ошибка: Свяжите пользователя джанго с пользователем бота (поле "Телеграм-пользователь менеджера")')
                logging.info('Ошибка: Свяжите пользователя джанго с пользователем бота (поле "Телеграм-пользователь менеджера")')



async def create_poll_option_user_info(option_id, bot_user_tg):
    url = f'{domen}api/create_option_user_info/'  # Замените на нужный URL

    async with aiohttp.ClientSession() as session:
        payload = {'option': option_id, 'bot_user_tg': bot_user_tg}
        async with session.post(url, data=payload) as response:
            return await response.json()


async def get_product_managers():
    url = f"{domen}api/product_managers/"
    auth = aiohttp.BasicAuth(admin_username, admin_password)
    
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                try:
                    data = random.choice(data)
                except:
                    data = {'username': admin_tg, 'user_id': admin_id}
                return data
            else:
                return None


async def some_async_function():
    # Ваш код, где вы хотите вызвать функцию get_categories_list()
    #a = await do_poll_mailing(poll_id='1', options=[('1', 'Первый'), ('2', 'Второй')], title='Что лучше?', media_paths=[r'C:\Users\hp\Desktop\job\media\GettyImages-531906282-5eb4b86361a94e8ebb72e26dbba44aa4_AhwE7Zv.jpg'])
    # a = await get_botusers()
    print(await get_product_managers())

if __name__ == "__main__":
    asyncio.run(some_async_function())

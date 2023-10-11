from aiogram import Bot, Dispatcher, executor, types
from bot import TOKEN
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random



bot = Bot(TOKEN)
dp = Dispatcher(bot)

def inline_k():
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text="1", callback_data="button1"),
        InlineKeyboardButton(text="2", callback_data="button2"),
    ]
    keyboard.add(*buttons)

    return keyboard


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    # media = [
    #     types.InputMediaPhoto(media=r''),
    #     types.InputMediaPhoto(media=r''),
    #     # Добавьте все необходимые фотографии в этот список
    # ]
    media = types.MediaGroup()
    media.attach_photo(types.InputFile(r'C:\Users\hp\Desktop\job\media\GettyImages-531906282-5eb4b86361a94e8ebb72e26dbba44aa4_AhwE7Zv.jpg'))
    media.attach_photo(types.InputFile(r'C:\Users\hp\Desktop\job\media\2023-05-02_15-12-54.png'))

    # Отправляем группу фотографий
    await bot.send_media_group(message.from_user.id, media=media)
    await bot.send_message(message.from_user.id, "Какое изображение лучше?", reply_markup=inline_k())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

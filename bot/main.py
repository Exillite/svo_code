import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils.deep_linking import decode_payload
from aiogram.filters import CommandStart, CommandObject
from aiogram.filters.command import Command
from aiogram.utils.deep_linking import create_start_link
from aiogram.methods.get_chat_member import GetChatMember
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


BASE_URL = "http://127.0.0.1:8000/api/"


async def serv(url: str, data: dict):
    ret = requests.post(BASE_URL + "user", json=data)
    return ret.text


bot = Bot(token="7850724608:AAGGeHWkZWigDi5VRlNIYH1rd_6U0Lj-1Y4")

dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message, command: CommandObject):
    await serv("user", {"tg_id": message.from_user.id})
    
    MenuBuilder = ReplyKeyboardBuilder()
    MenuBuilder.row(
        KeyboardButton(text="Мне нужны услуги креэйторов"),
        KeyboardButton(text="Я хочу творить и создавать!")
    )
    

    await message.answer("Привет! Это бот ArtMatch. Здесь мы поможем найти клиентов и творцов. ArtMatch специализируется на таких сферах, как фотография, литература, художественное искусство, музыка, вебдизайн и видео. Для начала давай определимся, что тебе нужно.", reply_markup=MenuBuilder.as_markup(resize_keyboard=True))


class Form(StatesGroup):
    name = State()
    social = State()
    description = State()
    prof = State()
    tags = State()
    media_type = State()
    media = State()


@dp.message(F.text == "Я хочу творить и создавать!")
async def create_bio(message: types.Message, state: FSMContext):
    try:
        await message.answer("Пожалуйста, ответь на несколько вопросов для создания АртВизитки", reply_markup=None)
        await message.answer("Какое имя указать в визитке?")
        
        await state.set_state(Form.name)
    except Exception as e:
        print(str(e))



@dp.message(Form.name)
async def get_name(message: types.Message, state: FSMContext):
    await serv("bio", {"tg_id": message.from_user.id, "name": message.text})
    await message.answer("Теперь отправь фотографию для создания аватара")
    await state.set_state(Form.name)


async def main():
    print("Starting bot.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
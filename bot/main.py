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


bot = Bot(token="7850724608:AAGGeHWkZWigDi5VRlNIYH1rd_6U0Lj-1Y4")

dp = Dispatcher()




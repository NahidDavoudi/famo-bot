from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    name = message.from_user.first_name if message.from_user else ""
    await message.answer(f"سلام {name} 👋\nربات آماده‌ست. برای راهنما /help بزن.")


@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer("دستورها:\n/start شروع\n/help راهنما\n\nهر متن دیگه‌ای بفرستی، همونو برمی‌گردونم.")


@router.message()
async def echo(message: Message):
    if message.text:
        await message.answer(message.text)
    else:
        await message.answer("فعلاً فقط پیام متنی رو پشتیبانی می‌کنم.")

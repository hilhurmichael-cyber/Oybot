import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# ===== ТВОИ НАСТРОЙКИ =====
BOT_TOKEN = "9000957505:AAEGEKUsvf_v9UiCi-HaySktu1rJU-7XCA4"
CHANNEL_ID = "@infokrajne" 
CHANNEL_URL = "https://t.me/infokrajne" 
STICKER_FILE_ID = "CAACAgQAAxkBAAEkeJ9q9N3zClSo-0PUU9mBAn-pBy5QegACIxwAAuTfaFLmL1JXmgUmfj0E" 
# ==========================

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

def is_subscribed(member) -> bool:
    return member.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR) or getattr(member, "is_member", False)

@dp.message(F.chat.type == "private", F.text)
async def on_any_message(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться на канал", url=CHANNEL_URL)],
        [InlineKeyboardButton(text="🎁 Я подписался — получить подарок", callback_data="check_sub")]
    ])
    await message.answer("🎁 Чтобы получить подарок, подпишись на канал и нажми кнопку ниже.", reply_markup=keyboard)

@dp.callback_query(F.data == "check_sub")
async def on_check_sub(callback: CallbackQuery):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=callback.from_user.id)
        if is_subscribed(member):
            await callback.message.answer_sticker(STICKER_FILE_ID)
            await callback.answer("Готово! Подарок отправлен 🎁")
        else:
            await callback.answer("Ты ещё не подписан(а). Подпишись и нажми кнопку снова.", show_alert=True)
    except TelegramBadRequest:
        await callback.answer("Ошибка: добавь бота админом в канал.", show_alert=True)
    except Exception as e:
        logging.exception(e)
        await callback.answer("Ошибка. Попробуй позже.", show_alert=True)

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

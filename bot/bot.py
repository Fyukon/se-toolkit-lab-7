import argparse
import asyncio
import sys
import os
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Ensure the 'bot' directory is in the python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from config import settings
    from handlers import (
        dispatch_command, handle_start, handle_help, 
        handle_health, handle_scores, handle_version, handle_labs
    )
    from services.llm import route_intent
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# --- Telegram Bot Part ---

async def start_handler(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Labs list", callback_data="btn_labs"))
    builder.row(types.InlineKeyboardButton(text="System status", callback_data="btn_health"))
    builder.row(types.InlineKeyboardButton(text="Ask LLM", callback_data="btn_help_text"))
    
    await message.answer(await handle_start(), reply_markup=builder.as_markup())

async def help_handler(message: types.Message):
    await message.answer(await handle_help())

async def health_handler(message: types.Message):
    await message.answer(await handle_health())

async def labs_handler(message: types.Message):
    await message.answer(await handle_labs())

async def scores_handler(message: types.Message, command: types.BotCommand = None):
    args = ""
    if hasattr(command, 'args') and command.args:
        args = command.args
    elif hasattr(message, 'text') and len(message.text.split()) > 1:
        args = " ".join(message.text.split()[1:])
    await message.answer(await handle_scores(args))

async def text_message_handler(message: types.Message):
    """Catch-all for natural language queries."""
    if message.text and not message.text.startswith("/"):
        status_msg = await message.answer("Thinking...")
        response = await route_intent(message.text)
        await status_msg.edit_text(response)

@F.callback_query.register()
async def callback_handler(callback: types.CallbackQuery):
    if callback.data == "btn_labs":
        await callback.message.answer(await handle_labs())
    elif callback.data == "btn_health":
        await callback.message.answer(await handle_health())
    elif callback.data == "btn_help_text":
        await callback.message.answer("Just ask me anything! For example: 'Which lab has the lowest pass rate?'")
    await callback.answer()

async def main():
    if not settings.BOT_TOKEN:
        print("BOT_TOKEN is not set in environment or .env.bot.secret/.env.bot.example")
        sys.exit(1)
        
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.message.register(start_handler, Command("start"))
    dp.message.register(help_handler, Command("help"))
    dp.message.register(health_handler, Command("health"))
    dp.message.register(labs_handler, Command("labs"))
    dp.message.register(scores_handler, Command("scores"))
    dp.message.register(text_message_handler, F.text)

    print("Bot is starting...")
    await dp.start_polling(bot)

# --- CLI Part ---

async def cli_mode(command_text: str):
    try:
        response = await dispatch_command(command_text)
        if response:
            print(response)
        else:
            print(f"Empty response for command: {command_text}")
    except Exception as e:
        print(f"Error executing command: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LMS Bot")
    parser.add_argument("--test", type=str, help="Run in test mode with a specific command")

    args = parser.parse_args()

    if args.test:
        asyncio.run(cli_mode(args.test))
    else:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("Bot stopped by user")
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)

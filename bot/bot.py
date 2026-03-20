import argparse
import asyncio
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from config import settings
from handlers.core import dispatch_command, handle_start, handle_help, handle_health, handle_scores

# --- Telegram Bot Part ---

async def start_handler(message: types.Message):
    await message.answer(handle_start())

async def help_handler(message: types.Message):
    await message.answer(handle_help())

async def health_handler(message: types.Message):
    await message.answer(handle_health())

async def scores_handler(message: types.Message, command: types.BotCommand = None):
    args = ""
    if hasattr(command, 'args') and command.args:
        args = command.args
    await message.answer(handle_scores(args))

async def main():
    if not settings.BOT_TOKEN:
        print("BOT_TOKEN is not set in environment or .env.bot.secret/.env.bot.example")
        sys.exit(1)
        
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.message.register(start_handler, Command("start"))
    dp.message.register(help_handler, Command("help"))
    dp.message.register(health_handler, Command("health"))
    dp.message.register(scores_handler, Command("scores"))

    print("Bot is starting...")
    await dp.start_polling(bot)

# --- CLI Part ---

def cli_mode(command_text: str):
    response = dispatch_command(command_text)
    print(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LMS Bot")
    parser.add_argument("--test", type=str, help="Run in test mode with a specific command")

    args = parser.parse_args()

    if args.test:
        cli_mode(args.test)
    else:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("Bot stopped by user")

# main.py
import os
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from messages.message_handler import handle_message


# Webhook version
# def webhook(request) -> str:
#     if request.method == "POST":
#         bot = Bot(token=os.environ["TELEGRAM_TOKEN"])
#         message = request.get_json(force=True)
#         update = Update.de_json(message, bot)
#         handle_message(update)
#     return "ok"


# Server version
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print('error')


async def start_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_message(update)


def init() -> None:
    token = os.environ["TELEGRAM_TOKEN"]
    application = Application.builder().token(token).build()

    application.add_error_handler(error_handler)
    application.add_handler(MessageHandler(filters.ALL, start_chat))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    load_dotenv()
    init()

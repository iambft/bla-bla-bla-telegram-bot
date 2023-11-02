import asyncio
import base64
import os
import random
from telegram import Message, Bot


def decision(probability: float) -> bool:
    return random.random() < probability


async def delay_message_sending(bot: Bot, chat_id: str, text: str, delay: int):
    await asyncio.sleep(delay)
    await bot.send_message(chat_id=chat_id, text=text)
    return


async def delay_message_replying(message: Message, text: str, delay: int):
    await asyncio.sleep(delay)
    await message.reply_text(text)
    return


def random_from_one_to_five_minutes_in_seconds():
    min_delay = 60
    max_delay = 300  # google cloud function a timeout setting was set to 360 sec
    random_delay = int(random.random() * max_delay)
    return random_delay if random_delay > min_delay else min_delay


def decode_base64(convert_sample: str):
    convert_bytes = convert_sample.encode("ascii")
    converted_bytes = base64.b64decode(convert_bytes)
    decoded_sample = converted_bytes.decode("ascii")
    return decoded_sample


def is_answer_to_bot(message: Message):
    bot_name = os.environ["TELEGRAM_USERNAME"]
    return message.reply_to_message \
        and message.reply_to_message.from_user \
        and message.reply_to_message.from_user.name == bot_name[:1]

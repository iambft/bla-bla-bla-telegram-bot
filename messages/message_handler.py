from random import choice

from telegram import Update, Message
from messages.answers.anime import Anime
from messages.answers.apologize import Apologize
from messages.answers.apologize_to_admin import ApologizeToAdmin
from messages.answers.condemn_your_anus import CondemnYourAnus
from messages.answers.happy_birthday import HappyBirthday
from messages.answers.joke import Joke
from messages.answers.message_start_with_bot import MessageStartWithBot
from messages.answers.random_condemn import RandomCondemn
from messages.answers.statistics import Statistics
from messages.answers.the_fool_himself import TheFoolHimself
from messages.message_holder import MessageHolder
from services.google_sheet_db import GoogleSheetDB

google_sheet_db = GoogleSheetDB()

answers = [
    Anime,
    Apologize,
    ApologizeToAdmin,
    CondemnYourAnus,
    TheFoolHimself,
    HappyBirthday,
    MessageStartWithBot,
    RandomCondemn,
    Statistics,
    Joke
]


async def handle_message(update: Update):
    message: Message = update.message
    google_sheet_db.put_message(message)

    if message is None:
        return

    if not hasattr(message, 'text') or message.text is None:
        return

    approved_answers = []
    message_holder = MessageHolder(message)

    for Answer in answers:
        answer = Answer(message_holder)
        if answer.is_proceed():
            if not approved_answers or approved_answers[len(approved_answers) - 1].priority.value == answer.priority.value:
                approved_answers.append(answer)
            if approved_answers[len(approved_answers) - 1].priority.value < answer.priority.value:
                approved_answers = [answer]

    if len(approved_answers):
        answer = choice(approved_answers)
        await answer.action()

import os
from constants.data_cell_constants import APOLOGIZE_ANSWER
from messages.answers.abstract import AnswerAbstract, AnswerPriorityEnum
from messages.helpers import is_answer_to_bot
from constants.message_keys_constants import APOLOGIZE_MESSAGE_KEYS
from services.spam_limitation import reply_to_message_with_spam_limitation


class Apologize(AnswerAbstract):
    priority = AnswerPriorityEnum.LOW

    def is_proceed(self) -> bool:
        bot_name = os.environ["TELEGRAM_USERNAME"]
        message = self.message_holder.message
        is_request_to_bot = is_answer_to_bot(message) or self.message_holder.is_text_contain([bot_name])
        is_ask_to_apologize = self.message_holder.is_text_contain(APOLOGIZE_MESSAGE_KEYS)
        return is_request_to_bot and is_ask_to_apologize

    async def action(self) -> None:
        message = self.message_holder.message
        text = 'вибачте'
        silent_hours = 0
        await reply_to_message_with_spam_limitation(message, text, APOLOGIZE_ANSWER, silent_hours)
        return


import os
from messages.answers.abstract import AnswerAbstract, AnswerPriorityEnum
from messages.helpers import is_answer_to_bot
from constants.message_keys_constants import APOLOGIZE_MESSAGE_KEYS


class ApologizeToAdmin(AnswerAbstract):
    priority = AnswerPriorityEnum.LOW

    def is_proceed(self) -> bool:
        bot_name = os.environ["TELEGRAM_USERNAME"]
        admin_name = os.environ["ADMIN_TELEGRAM_USERNAME"]
        message = self.message_holder.message
        message_from = self.message_holder.from_user_name
        is_admin = message_from == admin_name
        is_request_to_bot = is_answer_to_bot(message) or self.message_holder.is_text_contain([bot_name])
        is_ask_to_apologize = self.message_holder.is_text_contain(APOLOGIZE_MESSAGE_KEYS)
        return is_admin and is_request_to_bot and is_ask_to_apologize

    async def action(self) -> None:
        message = self.message_holder.message
        text = 'вибачте хозяін'
        await message.reply_text(text)
        return

from constants.data_cell_constants import ANIME_LAST_MESSAGE_CELL
from messages.answers.abstract import AnswerAbstract, AnswerPriorityEnum
from constants.message_keys_constants import ANIME_MESSAGE_KEYS
from services.spam_limitation import reply_to_message_with_spam_limitation


class Anime(AnswerAbstract):
    priority = AnswerPriorityEnum.LOW

    def is_proceed(self) -> bool:
        return self.message_holder.is_text_contain(ANIME_MESSAGE_KEYS)

    async def action(self) -> None:
        message = self.message_holder.message
        text = 'засуджую'
        silent_hours = 3
        await reply_to_message_with_spam_limitation(message, text, ANIME_LAST_MESSAGE_CELL, silent_hours)
        return

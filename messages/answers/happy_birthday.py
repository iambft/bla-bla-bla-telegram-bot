from constants.data_cell_constants import HAPPY_BIRTHDAY_MESSAGE_CELL
from messages.answers.abstract import AnswerAbstract, AnswerPriorityEnum
from messages.helpers import random_from_one_to_five_minutes_in_seconds
from constants.message_keys_constants import HAPPY_BIRTHDAY_MESSAGE_KEYS
from services.spam_limitation import send_message_with_spam_limitation


class HappyBirthday(AnswerAbstract):
    priority = AnswerPriorityEnum.LOW

    def is_proceed(self) -> bool:
        return self.message_holder.is_text_contain(HAPPY_BIRTHDAY_MESSAGE_KEYS)

    async def action(self) -> None:
        text = 'Вітаю з Днем Народження!'
        silent_hours = 6
        message = self.message_holder.message
        message_delay_seconds = random_from_one_to_five_minutes_in_seconds()
        await send_message_with_spam_limitation(
            message,
            text,
            HAPPY_BIRTHDAY_MESSAGE_CELL,
            silent_hours,
            message_delay_seconds
        )
        return

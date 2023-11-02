from constants.data_cell_constants import JOKE_CELL_1, JOKE_CELL_2
from messages.answers.abstract import AnswerAbstract, AnswerPriorityEnum
from constants.message_keys_constants import ASK_FOR_JOKE
from services.spam_limitation import send_message_with_spam_limitation


class Joke(AnswerAbstract):
    priority = AnswerPriorityEnum.LOW

    def is_proceed(self) -> bool:
        return self.message_holder.is_text_contain(ASK_FOR_JOKE)

    async def action(self) -> None:
        message = self.message_holder.message
        text_first_part = 'Йде ведмідь по лісу і бічить машина горить'
        text_second_part = 'сів в машину і згорів'
        silent_hours = 6
        pause_seconds = 120
        await send_message_with_spam_limitation(message, text_first_part, JOKE_CELL_1, silent_hours)
        await send_message_with_spam_limitation(message, text_second_part, JOKE_CELL_2, silent_hours, pause_seconds)
        return

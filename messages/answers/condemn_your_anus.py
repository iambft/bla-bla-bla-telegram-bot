from random import choice
from constants.data_cell_constants import ANUS_ANSWER
from messages.answers.abstract import AnswerAbstract, AnswerPriorityEnum
from constants.message_keys_constants import ANUS_CONDEMN_P1_KEYS, ANUS_CONDEMN_P2_KEYS, ANUS_CONDEMN_P3_KEYS
from services.spam_limitation import reply_to_message_with_spam_limitation


class CondemnYourAnus(AnswerAbstract):
    priority = AnswerPriorityEnum.LOW

    def is_proceed(self) -> bool:
        is_contain_p_1 = self.message_holder.is_text_contain(ANUS_CONDEMN_P1_KEYS)
        is_contain_p_2 = self.message_holder.is_text_contain(ANUS_CONDEMN_P2_KEYS)
        is_contain_p_3 = self.message_holder.is_text_contain(ANUS_CONDEMN_P3_KEYS)
        return is_contain_p_1 and is_contain_p_2 and is_contain_p_3

    async def action(self) -> None:
        text = anus_answer()
        message = self.message_holder.message
        silent_hours = 0
        await reply_to_message_with_spam_limitation(message, text, ANUS_ANSWER, silent_hours)
        return


def anus_answer():
    return choice(['нема анусу нема засудження', 'добре босс', 'нє', 'укусі мой залізний зад'])

from messages.answers.abstract import AnswerAbstract, AnswerPriorityEnum
from constants.message_keys_constants import PUNCH_BOT_MESSAGE_KEYS


class TheFoolHimself(AnswerAbstract):
    priority = AnswerPriorityEnum.LOW

    def is_proceed(self) -> bool:
        return self.message_holder.is_text_contain(PUNCH_BOT_MESSAGE_KEYS)

    async def action(self) -> None:
        text = 'сам дурак'
        message = self.message_holder.message
        await message.reply_text(text)
        return

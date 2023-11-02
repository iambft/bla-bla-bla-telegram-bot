from messages.answers.abstract import AnswerAbstract, AnswerPriorityEnum
from messages.helpers import decision


class RandomCondemn(AnswerAbstract):
    priority = AnswerPriorityEnum.LOW

    def is_proceed(self) -> bool:
        return decision(0.005)

    async def action(self) -> None:
        message = self.message_holder.message
        await message.reply_text('засуджую')
        return

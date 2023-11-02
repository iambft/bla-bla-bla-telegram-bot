from messages.answers.abstract import AnswerAbstract, AnswerPriorityEnum


class MessageStartWithBot(AnswerAbstract):
    priority = AnswerPriorityEnum.LOW

    def is_proceed(self) -> bool:
        return self.message_holder.text.startswith('бот')

    async def action(self) -> None:
        message = self.message_holder.message
        await reach_out_bot(message)
        return


async def reach_out_bot(message):
    text: str = message.text
    processed: str = text.lower()
    list_of_words = processed.split()
    if len(list_of_words) > 1:
        next_word = list_of_words[1]
        msg = f'сам {next_word}'
        if next_word == 'ти':
            next_next_word = list_of_words[2]
            msg = f'сам {next_word} {next_next_word}'
        await message.reply_text(msg)

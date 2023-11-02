from enum import Enum

from messages.message_holder import MessageHolder


class AnswerPriorityEnum(Enum):
    BASE = 0
    LOW = 1
    MEDIUM = 2
    HEIGHT = 3


class AnswerAbstract:
    priority: AnswerPriorityEnum
    message_holder: MessageHolder

    def __init__(self, message_holder: MessageHolder):
        self.message_holder = message_holder

    def is_proceed(self) -> bool:
        return False

    async def action(self) -> None:
        return



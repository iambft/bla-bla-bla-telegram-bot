from telegram import Message


class MessageHolder:
    message: Message
    text: str
    from_user_name: str

    def __init__(self, message: Message):
        self.message = message
        self.text: str = message.text and message.text.lower()
        self.from_user_name = message.from_user and message.from_user.name

    def is_text_contain(self, substrings: [str]):
        return any([x in self.text for x in substrings])

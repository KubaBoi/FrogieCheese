from cheese.modules.cheeseModel import CheeseModel

#@model
class ChatT(CheeseModel):

    def __init__(self, id=None, user_id=None, chat_id=None, last_delivered_message_id=None, last_seen_message_id=None):
        self.id = id
        self.user_id = user_id
        self.chat_id = chat_id
        self.last_delivered_message_id = last_delivered_message_id
        self.last_seen_message_id = last_seen_message_id
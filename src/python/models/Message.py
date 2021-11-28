from cheese.modules.cheeseModel import CheeseModel

#@model
class Message(CheeseModel):

    def __init__(self, id=None, author_id=None, content=None, chat_id=None, time_stamp=None):
        self.id = id
        self.author_id = author_id
        self.content = content
        self.chat_id = chat_id
        self.time_stamp = time_stamp

    def toJson(self):
        response = {
            "ID": self.id,
            "AUTHOR_ID": self.author_id,
            "CONTENT": self.content,
            "CHAT_ID": self.chat_id,
            "TIME_STAMP": self.time_stamp
        }
        return response
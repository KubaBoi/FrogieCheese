from cheese.modules.cheeseModel import CheeseModel

#@model
class Chat(CheeseModel):

    def __init__(self, id=None, chat_name=None, last_activity=None, picture_id=None):
        self.id = id
        self.chat_name = chat_name
        self.last_activity = last_activity
        self.picture_id = picture_id

        self.chat_users = []

    def toJson(self):
        users = []
        for user in self.chat_users:
            users.append(user.toJson())

        response = {
            "ID": self.id,
            "CHAT_NAME": self.chat_name,
            "LAST_ACTIVITY": self.last_activity,
            "PICTURE_ID": self.picture_id,
            "CHAT_USERS": users
        }
        return response
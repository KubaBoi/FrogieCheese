from cheese.modules.cheeseModel import CheeseModel

#@model
class User(CheeseModel):

    def __init__(self, id=None, user_name=None, email=None, picture_id=None):
        self.id = id
        self.user_name = user_name
        self.email = email
        self.picture_id = picture_id

    def toJson(self):
        response = {
            "ID": self.id,
            "USER_NAME": self.user_name,
            "EMAIL": self.email,
            "PICTURE_ID": self.picture_id
        }
        return response
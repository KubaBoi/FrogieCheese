from cheese.modules.cheeseModel import CheeseModel

#@model
class Token(CheeseModel):

    def __init__(self, id=None, token=None, user_id=None, ip=None, end_time=None):
        self.id = id
        self.token = token
        self.user_id = user_id
        self.ip = ip
        self.end_time = end_time

    def toJson(self):
        response = {
            "ID": self.id,
            "TOKEN": self.token,
            "USER_ID": self.user_id,
            "IP": self.ip,
            "END_TIME": self.end_time
        }
        return response
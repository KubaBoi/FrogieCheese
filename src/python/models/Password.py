from cheese.modules.cheeseModel import CheeseModel

#@model
class Password(CheeseModel):

    def __init__(self, id=None, user_id=None, password=None, duration=None):
        self.id = id
        self.user_id = user_id
        self.password = password
        self.duration = duration
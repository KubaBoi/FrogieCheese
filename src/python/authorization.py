from urllib.parse import unquote
from cheese.modules.cheeseController import CheeseController

#@authorization enabled
class Authorization:

    @staticmethod
    def authorize(server, path, method):
        print(path, method)
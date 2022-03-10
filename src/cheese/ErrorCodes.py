
from cheese.modules.cheeseController import CheeseController

class Error:
    
    @staticmethod
    def init():
        Error.BadJson = CheeseController.createResponse({"ERROR": "Wrong json structure"}, 400) # Bad request
        Error.OldPass = CheeseController.createResponse({"ERROR": "Old password"}, 401) # Unauthorized
        Error.BadCred = CheeseController.createResponse({"ERROR": "Wrong credentials"}, 401) # Unauthorized
        Error.BadToken = CheeseController.createResponse({"ERROR": "Unable to authorize with this token"}, 401) # Unauthorized
        Error.AccDenied = CheeseController.createResponse({"ERROR": "Access denied"}, 401) # Unathorized
        Error.FileNotFound = CheeseController.createResponse({"ERROR": "File not found"}, 404) # File not found

    @staticmethod
    def sendCustomError(server, comment, code):
        response = CheeseController.createResponse({"ERROR": comment}, code)
        CheeseController.sendResponse(server, response)


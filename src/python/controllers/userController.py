#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cheese.modules.cheeseController import CheeseController
from cheese.ErrorCodes import Error
from python.controllers.authenticationController import AuthenticationController
from python.controllers.chatController import ChatController

from python.repositories.chatRepository import ChatRepository
from python.repositories.passwordRepository import PasswordRepository
from python.repositories.userRepository import UserRepository
from python.repositories.chatTRepository import ChatTRepository
from python.repositories.messageRepository import MessageRepository

#@controller /users
class UserController(CheeseController):

    @staticmethod
    def init():
        UserController.PASSWORD_DURATION = 432000 # 5 days

    #@post /createUser
    @staticmethod
    def createUser(server, path, auth):
        args = auth["args"]

        # bad json
        if (not CheeseController.validateJson(["USER_NAME", "PASSWORD", "EMAIL"], args)):
            CheeseController.sendResponse(server, Error.BadJson)
            return

        # OK
        userName = args["USER_NAME"]
        password = args["PASSWORD"]
        email = args["EMAIL"]

        if (not UserRepository.validateUserName(userName)):
            Error.sendCustomError(server, "Name is already taken", 409)
            return

        userId = UserRepository.findNewId()
        passId = PasswordRepository.findNewId()

        user = (userId, userName, email, 5)
        UserRepository.save(user)
        passW = (passId, userId, password, AuthenticationController.getTime(UserController.PASSWORD_DURATION))
        PasswordRepository.save(passW)

        user = UserRepository.findUserById(userId)
        response = CheeseController.createResponse({"USER": user}, 200)
        CheeseController.sendResponse(server, response)

    #@post /getUser
    @staticmethod
    def getUser(server, path, auth):
        if (auth == None):
            return
        args = auth["args"]

        # bad json
        if (not CheeseController.validateJson(["USER_ID"], args)):
            CheeseController.sendResponse(server, Error.BadJson)
            return

        # OK
        userId = args["USER_ID"]

        user = UserRepository.findUserById(userId)
        if (user == None):
            Error.sendCustomError(server, "Unknown user", 404)
            return
        
        response = CheeseController.createResponse({"USER": user}, 200)
        CheeseController.sendResponse(server, response)

    #@post /getUserByName
    @staticmethod
    def getUserByName(server, path, auth):
        if (auth == None):
            return
        args = auth["args"]

        # bad json
        if (not CheeseController.validateJson(["USER_NAME"], args)):
            CheeseController.sendResponse(server, Error.BadJson)
            return

        # OK
        userName = args["USER_NAME"]

        user = UserRepository.findUserByName(userName)
        if (user == None):
            Error.sendCustomError(server, "Uknown user", 404)
            return

        response = CheeseController.createResponse({"USER": user}, 200)
        CheeseController.sendResponse(server, response)

    #@post /update
    @staticmethod
    def update(server, path, auth):
        if (auth == None):
            return

        # OK
        connectedUser = auth["user"]
        ip = auth["ip"]
        token = auth["token"]

        AuthenticationController.updateToken(ip, token)

        response = CheeseController.createResponse({"CHANGES": ChatController.getChanges(connectedUser["id"])}, 200)
        CheeseController.sendResponse(server, response)

    #@post /getUserDynamic
    @staticmethod
    def getUserDynamic(server, path, auth):
        if (auth == None):
            return
        args = auth["args"]

        # bad json
        if (not CheeseController.validateJson(["USER_NAME_START"], args)):
            CheeseController.sendResponse(server, Error.BadJson)
            return

        # OK
        userNameStart = args["USER_NAME_START"]

        users = UserRepository.findUsersDynamic(userNameStart.lower() + "%")

        response = CheeseController.createResponse({"USERS": users}, 200)
        CheeseController.sendResponse(server, response)

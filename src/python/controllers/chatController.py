#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cheese.modules.cheeseController import CheeseController
from cheese.ErrorCodes import Error
from python.controllers.authenticationController import AuthenticationController

from python.repositories.chatRepository import ChatRepository
from python.repositories.userRepository import UserRepository
from python.repositories.chatTRepository import ChatTRepository

#@controller /chats
class ChatController(CheeseController):

    @staticmethod
    def init():
        ChatController.MAX_SENDED_CHATS = 20

    #@post /getChats
    @staticmethod
    def getChats(server, path, auth):
        if (auth == None):
            return
        args = CheeseController.readArgs(server)

        # bad json
        if (not CheeseController.validateJson(["FROM_TIME"], args)):
            CheeseController.sendResponse(server, Error.BadJson)
            return

        # OK
        connectedUser = auth["user"]
        fromTime = args["FROM_TIME"]

        if (fromTime == 0):
            fromTime = AuthenticationController.getTime(0)

        chats = ChatRepository.findChatsFrom(connectedUser["id"], fromTime, ChatController.MAX_SENDED_CHATS)
        response = CheeseController.createResponse({"CHATS": chats}, 200)

        CheeseController.sendResponse(server, response)

    #@post /getChatsId
    @staticmethod
    def getChatsById(server, path, auth):
        if (auth == None):
            return
        args = CheeseController.readArgs(server)

        # bad json
        if (not CheeseController.validateJson(["CHAT_IDS"], args)):
            CheeseController.sendResponse(server, Error.BadJson)
            return

        # OK
        ids = args["CHAT_IDS"]
        connectedUser = auth["user"]

        chats = ChatRepository.findChatsByIds(ids)
        response = CheeseController.createResponse({"CHATS": chats}, 200)

        CheeseController.sendResponse(server, response)

    #@post /createChat
    @staticmethod
    def createChat(server, path, auth):
        if (auth == None):
            return
        args = CheeseController.readArgs(server)

        # bad json
        if (not CheeseController.validateJson(["CHAT_USERS"], args)):
            CheeseController.sendResponse(server, Error.BadJson)
            return

        # OK
        usersIds = args["CHAT_USERS"]
        connectedUser = auth["user"]
    
        users = []
        for userId in usersIds:
            if (ChatRepository.doesChatExists(connectedUser["id"], userId) and userId != connectedUser["id"]):
                Error.sendCustomError(server, "Chat already exists", 409) # Conflict
                return
            
            user = UserRepository.findUserById(userId)
            if (user == None):
                Error.sendCustomError(server, "User does not exists", 409) # Conflict
                return
            users.append(user)

        chatName = ""
        chatId = ChatRepository.findNewId()
        newChat = (
                chatId,
                chatName,
                AuthenticationController.getTime(),
                5
            )
        ChatRepository.save(newChat)

        for userId in usersIds:
            newChatT = (
                ChatTRepository.findNewId(),
                userId,
                chatId,
                None,
                None
            )
            ChatTRepository.save(newChatT)

        response = CheeseController.createResponse({"CHAT": newChat}, 200)

        CheeseController.sendResponse(server, response)


    #METHODS

    @staticmethod
    def updateChat(chatId):
        chat = ChatRepository.findChatById(chatId)
        ChatRepository.update((chat["id"], chat["chat_name"], AuthenticationController.getTime(), chat["picture_id"]))

    @staticmethod
    def getChanges(userId):
        chats = ChatTRepository.findUndeliveredChatsByUserId(userId)
        return chats




    
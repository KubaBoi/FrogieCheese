#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cheese.modules.cheeseController import CheeseController
from cheese.ErrorCodes import Error
from python.controllers.authenticationController import AuthenticationController

from python.repositories.chatRepository import ChatRepository
from python.repositories.messageRepository import MessageRepository
from python.repositories.userRepository import UserRepository
from python.repositories.chatTRepository import ChatTRepository

from python.models.Chat import Chat
from python.models.Message import Message
from python.models.ChatT import ChatT

#@controller /chats
class ChatController(CheeseController):

    MAX_SENDED_CHATS = 20

    #@post /getChats
    @staticmethod
    def getChats(server, path, auth):
        if (auth == None):
            return
        args = auth["args"]

        # bad json
        if (not CheeseController.validateJson(["FROM_TIME"], args)):
            CheeseController.sendResponse(server, Error.BadJson)
            return

        # OK
        connectedUser = auth["user"]
        fromTime = args["FROM_TIME"]

        if (fromTime == 0):
            fromTime = AuthenticationController.getTime(0)

        chats = ChatRepository.findChatsFrom(connectedUser.id, fromTime, ChatController.MAX_SENDED_CHATS)
        jsonArray = []
        for chat in chats:
            chatUsers = ChatTRepository.findAllUsersFromChat(chat.id)
            users = []
            for user in chatUsers:
                users.append(UserRepository.findUserById(user.user_id))

            chat.chat_users = users
            jsonArray.append(chat.toJson())

        response = CheeseController.createResponse({"CHATS": jsonArray}, 200)
        CheeseController.sendResponse(server, response)

    #@post /getChatsById
    @staticmethod
    def getChatsById(server, path, auth):
        if (auth == None):
            return
        args = auth["args"]

        # bad json
        if (not CheeseController.validateJson(["CHAT_IDS"], args)):
            CheeseController.sendResponse(server, Error.BadJson)
            return

        # OK
        ids = args["CHAT_IDS"]
        connectedUser = auth["user"]

        chats = ChatRepository.findChatsByIds(ids)
        jsonArray = []
        for chat in chats:
            jsonArray.append(chat.toJson())
        response = CheeseController.createResponse({"CHATS": jsonArray}, 200)

        CheeseController.sendResponse(server, response)

    #@post /createChat
    @staticmethod
    def createChat(server, path, auth):
        if (auth == None):
            return
        args = auth["args"]

        # bad json
        if (not CheeseController.validateJson(["CHAT_USERS"], args)):
            CheeseController.sendResponse(server, Error.BadJson)
            return

        # OK
        usersIds = args["CHAT_USERS"]
        connectedUser = auth["user"]
    
        users = []
        for userId in usersIds:
            if (ChatRepository.doesChatExists(connectedUser.id, userId) and userId != connectedUser.id):
                Error.sendCustomError(server, "Chat already exists", 409) # Conflict
                return
            
            user = UserRepository.findUserById(userId)
            if (user == None):
                Error.sendCustomError(server, "User does not exists", 409) # Conflict
                return
            users.append(user)

        chatName = ""
        chatId = ChatRepository.findNewId()
        newChat = Chat(
                chatId,
                chatName,
                AuthenticationController.getTime(),
                5
            )
        ChatRepository.save(newChat)

        messageId = MessageRepository.findNewId()
        firstMessage = Message(messageId, connectedUser.id, "Ahoj", chatId, AuthenticationController.getTime())
        MessageRepository.save(firstMessage)

        for userId in usersIds:
            newChatT = ChatT(
                ChatTRepository.findNewId(),
                userId,
                chatId,
                messageId,
                messageId
            )
            ChatTRepository.save(newChatT)

        response = CheeseController.createResponse({"CHAT": newChat.toJson()}, 200)

        CheeseController.sendResponse(server, response)


    #METHODS

    @staticmethod
    def updateChat(chatId):
        chat = ChatRepository.findChatById(chatId)
        chat.last_activity = AuthenticationController.getTime()
        ChatRepository.update(chat)

    @staticmethod
    def getChanges(userId):
        chats = ChatTRepository.findUndeliveredChatsByUserId(userId)
        return chats




    
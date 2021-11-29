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
            chatUsers = ChatTRepository.findAllUsersFromChat(chat.id)
            users = []
            for user in chatUsers:
                users.append(UserRepository.findUserById(user.user_id))
            
            chat.chat_users = users
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
        userNames = []
        for userId in usersIds:            
            user = UserRepository.findUserById(userId)
            if (user == None):
                Error.sendCustomError(server, "User does not exists", 409) # Conflict
                return
            users.append(user)
            userNames.append(user.user_name)

        chatName = ", ".join(userNames)
        chatId = ChatRepository.findNewId()
        newChat = Chat(
                chatId,
                chatName,
                AuthenticationController.getTime(),
                0
            )
        ChatRepository.save(newChat)

        messageId = MessageRepository.findNewId()
        firstMessage = Message(
            messageId,
            connectedUser.id, 
            "Nikdy nikomu neposílej svoje přihlašovací údaje. V případě komunikace s podporou se na tvoje heslo žabičky nikdy ptát nebudou.", 
            chatId, 
            AuthenticationController.getTime()
        )
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

        chatUsers = ChatTRepository.findAllUsersFromChat(newChat.id)
        users = []
        for user in chatUsers:
            users.append(UserRepository.findUserById(user.user_id))
        
        newChat.chat_users = users

        response = CheeseController.createResponse({"CHAT": newChat.toJson()}, 200)

        CheeseController.sendResponse(server, response)

    #@post /addUser
    @staticmethod
    def addUser(server, path, auth):
        if (auth == None):
            return
        args = auth["args"]

        # bad json
        if (not CheeseController.validateJson(["CHAT_ID", "USER_ID"], args)):
            CheeseController.sendResponse(server, Error.BadJson)
            return

        # OK
        chatId = args["CHAT_ID"]
        userId = args["USER_ID"]
        connectedUser = auth["user"]

        chat = ChatRepository.findChatById(chatId)
        if (chat == None):
            Error.sendCustomError(server, "Chat does not exist", 409) # Conflict
            return

        usersChatT = ChatTRepository.findChatTByUserIdAndChatId(connectedUser.id, chat.id)
        chatTid = ChatTRepository.findNewId()
        chatT = ChatT(chatTid, userId, chat.id, usersChatT.last_delivered_message_id, usersChatT.last_seen_message_id)
        ChatTRepository.save(chatT)

        chatUsers = ChatTRepository.findAllUsersFromChat(chat.id)
        users = []
        for user in chatUsers:
            users.append(UserRepository.findUserById(user.user_id))

        chat.chat_users = users

        response = CheeseController.createResponse({"CHAT": chat.toJson()}, 200)

        CheeseController.sendResponse(server, response)

    #@post /renameChat
    @staticmethod
    def renameChat(server, path, auth):
        if (auth == None):
            return
        args = auth["args"]

        # bad json
        if (not CheeseController.validateJson(["CHAT_ID", "NAME"], args)):
            CheeseController.sendResponse(server, Error.BadJson)
            return

        #OK
        name = args["NAME"]
        chatId = args["CHAT_ID"]

        chat = ChatRepository.findChatById(chatId)
        if (chat == None):
            Error.sendCustomError(server, "Chat does not exist", 409) # Conflict
            return

        chat.chat_name = name
        ChatRepository.update(chat)

        response = CheeseController.createResponse({"CHAT_ID": chatId}, 200)
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




    
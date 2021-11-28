#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cheese.modules.cheeseController import CheeseController
from cheese.ErrorCodes import Error
from python.controllers.authenticationController import AuthenticationController
from python.controllers.chatController import ChatController
from python.models.Message import Message

from python.repositories.chatRepository import ChatRepository
from python.repositories.userRepository import UserRepository
from python.repositories.chatTRepository import ChatTRepository
from python.repositories.messageRepository import MessageRepository

#@controller /messages
class MessageController(CheeseController):

    MAX_SENDED_MESSAGES = 20

    #@post /getChatMessages
    def getChatMessages(server, path, auth):
        if (auth == None):
            return
        args = auth["args"]

        # bad json
        if (not CheeseController.validateJson(["FROM_TIME", "CHATS"], args)):
            CheeseController.sendResponse(server, Error.BadJson)
            return

        # OK
        chatIds = args["CHATS"]
        fromTime = args["FROM_TIME"]
        connectedUser = auth["user"]

        chatsArray = []
        for chatId in chatIds:
            if (chatId == None):
                continue

            # authorize if chat belongs to user
            if (not ChatRepository.belongsToUserId(connectedUser.id, chatId)):
                CheeseController.sendResponse(server, Error.AccDenied)
                return

            if (fromTime == 0):
                fromTime = AuthenticationController.getTime()

            chatResponse = {}
            messages = MessageRepository.findMessagesFrom(chatId, fromTime, MessageController.MAX_SENDED_MESSAGES)

            chatT = ChatTRepository.findChatTByUserIdAndChatId(connectedUser.id, chatId)
            if (chatT.last_delivered_message_id != None):
                lastDeliveredMessage = MessageRepository.findById(chatT.last_delivered_message_id)

                if (lastDeliveredMessage.time_stamp > messages[0].time_stamp):
                    Error.sendCustomError(server, "Message is older than last seen, nothing is happening :)", 418)
                    return

            if (len(messages) > 0):
                chatT.last_delivered_message_id = messages[0].id
            ChatTRepository.update(chatT)

            messagesJson = []
            for message in messages:
                messagesJson.append(message.toJson())

            chatResponse["MESSAGES"] = messagesJson
            chatResponse["LAST_DELIVERED_MESSAGE_ID"] = chatT.last_delivered_message_id
            chatResponse["LAST_SEEN_MESSAGE_ID"] = chatT.last_seen_message_id
            chatResponse["CHAT_ID"] = chatId

            chatsArray.append(chatResponse)

        response = CheeseController.createResponse({"CHATS": chatsArray}, 200)
        CheeseController.sendResponse(server, response)

    #@post /sendMessage
    @staticmethod
    def sendMessage(server, path, auth):
        if (auth == None):
            return
        args = auth["args"]

        # bad json
        if (not CheeseController.validateJson(["CHAT_ID", "CONTENT"], args)):
            CheeseController.sendResponse(server, Error.BadJson)
            return

        # OK
        chatId = args["CHAT_ID"]
        content = args["CONTENT"]
        connectedUser = auth["user"]

        # authorize if chat belongs user
        if (not ChatRepository.belongsToUserId(connectedUser.id, chatId)):
            CheeseController.sendResponse(server, Error.AccDenied)
            return

        messageId = MessageRepository.findNewId()

        message = Message(messageId, connectedUser.id, content, chatId, AuthenticationController.getTime())
        MessageRepository.save(message)
        message = MessageRepository.findById(messageId)
        ChatController.updateChat(chatId)

        chatT = ChatTRepository.findChatTByUserIdAndChatId(connectedUser.id, chatId)
        chatT.last_seen_message_id = messageId
        chatT.last_delivered_message_id = messageId
        ChatTRepository.update(chatT)

        response = CheeseController.createResponse({"MESSAGE": message.toJson()}, 200)
        CheeseController.sendResponse(server, response)

    #@post /seenMessage
    @staticmethod
    def seenMessage(server, path, auth):
        if (auth == None):
            return
        args = auth["args"]

        # bad json
        if (not CheeseController.validateJson(["MESSAGE_ID"], args)):
            CheeseController.sendResponse(server, Error.BadJson)
            return

        # OK
        messageId = args["MESSAGE_ID"]
        connectedUser = auth["user"]

        message = MessageRepository.findById(messageId)
        if (message == None):
            Error.sendCustomError(server, "Message not found", 404)
            return

        if (ChatRepository.belongsToUserId(connectedUser.id, message.id)):
            CheeseController.sendResponse(server, Error.AccDenied)
            return

        chatT = ChatTRepository.findChatTByUserIdAndChatId(connectedUser.id, message.chat_id)

        if (chatT.last_seen_message_id != None):
            lastSeenMessage = MessageRepository.findById(chatT.last_seen_message_id)

            if (lastSeenMessage.time_stamp > message.time_stamp):
                Error.sendCustomError(server, "Message is older than last seen, nothing is happening :)", 418)
                return

        chatT.last_delivered_message_id = message.id
        chatT.last_seen_message_id = message.id
        ChatTRepository.update(chatT)

        response = CheeseController.createResponse({"MESSAGE": message.toJson()}, 200)
        CheeseController.sendResponse(server, response)


            
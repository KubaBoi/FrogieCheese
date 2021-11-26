#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cheese.modules.cheeseController import CheeseController
from cheese.ErrorCodes import Error
from python.controllers.authenticationController import AuthenticationController

from python.repositories.chatRepository import ChatRepository
from python.repositories.userRepository import UserRepository
from python.repositories.chatTRepository import ChatTRepository
from python.repositories.messageRepository import MessageRepository

#@controller /messages
class MessageController(CheeseController):

    @staticmethod
    def init():
        MessageController.MAX_SENDED_MESSAGES = 20

    #@post /getChatMessages
    def getChatMessages(server, path, auth):
        if (auth == None):
            return
        args = CheeseController.readArgs(server)

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
            # authorize if chat belongs to user
            if (not ChatRepository.belongsToUserId(connectedUser["id"], chatId)):
                CheeseController.sendResponse(server, Error.AccDenied)
                return

            if (fromTime == 0):
                fromTime = AuthenticationController.getTime()

            chatResponse = {}
            messages = MessageRepository.findMessagesFrom(chatId, fromTime, MessageController.MAX_SENDED_MESSAGES)

            chatT = ChatTRepository.findChatTByUserIdAndChatId(connectedUser["id"], chatId)
            if (chatT["last_delivered_message_id"] != None):
                lastDeliveredMessage = MessageRepository.findById(chatT["last_delivered_message_id"])

                if (lastDeliveredMessage["time_stamp"] > messages[0]["time_stamp"]):
                    Error.sendCustomError(server, "Message is older than last seen, nothing is happening :)", 418)


            





            
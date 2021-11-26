#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cheese.modules.cheeseRepository import CheeseRepository

#@repository chats_t
#@dbscheme (id, user_id, chat_id, last_delivered_message_id, last_seen_message_id)
class ChatTRepository(CheeseRepository):

    #@query "select * from chats_t ct where ct.user_id = :userId and ct.chat_id = :chatId;"
    #@return one
    @staticmethod
    def findChatTByUserIdAndChatId(userId, chatId):
        return CheeseRepository.findChatTByUserIdAndChatId([userId, chatId])

    #@query "select * from chats_t ct where ct.user_id = :userId;"
    #@return array
    @staticmethod
    def findChatsByUserID(userId):
        return CheeseRepository.findChatsByUserID([userId])

    #@query "select ct.id, ct.user_id, ct.chat_id, ct.last_delivered_message_id, ct.last_seen_message_id from chats_t ct
    #        where ct.user_id = :userId and
    #        (ct.last_delivered_message_id is NULL or
    #        exists
    #        (select ct2.id from chats_t ct2
    #        inner join messages m
    #        on m.id = ct2.last_delivered_message_id
    #        where ct2.user_id = :userId and exists
    #        (select m2.id from messages m2
    #        where m2.time_stamp > m.time_stamp and m2.chat_id = ct2.chat_id)));"
    #@return array
    @staticmethod
    def findUndeliveredChatsByUserId(userId):
        return CheeseRepository.findUndeliveredChatsByUserId([userId])

    #@query "select count(*) from chats_t;"
    #@return num
    @staticmethod
    def findNewId():
        return CheeseRepository.findNewId([])

    #@query "select * from chats_t ct where ct.chat_id = :chatId;"
    #@return array
    @staticmethod
    def findAllUsersFromChat(chatId):
        return CheeseRepository.findAllUsersFromChat([chatId])

    @staticmethod
    def save(obj):
        return CheeseRepository.save([obj])
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cheese.modules.cheeseRepository import CheeseRepository

#@repository messages
#@dbscheme (id, author_id, content, chat_id, time_stamp)
class MessageRepository(CheeseRepository):

    #@query "select distinct m.id, author_id, content, m.chat_id, m.time_stamp from messages m
    #                inner join chats c
    #                on c.id = m.chat_id
    #                inner join chats_t ct
    #                on ct.chat_id = c.id
    #                inner join users u
    #                on u.id = ct.user_id
    #                where c.id = :chatId and m.time_stamp <= :timeStamp
    #                order by m.time_stamp desc
    #                limit :messagesCount;"
    #@return array
    @staticmethod
    def findMessagesFrom(chatId, timeStamp, messagesCount):
        return CheeseRepository.findMessagesFrom([chatId, timeStamp, messagesCount])

    #@query "select count(*) from messages;"
    #@return num
    @staticmethod
    def findNewId():
        return CheeseRepository.findNewId([])

    #@query "select * from messages m where m.id = :messageId;"
    #@return one
    @staticmethod
    def findById(messageId):
        return CheeseRepository.findById([messageId])

    @staticmethod
    def save(obj):
        return CheeseRepository.save([obj])
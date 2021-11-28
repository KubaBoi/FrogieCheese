#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cheese.modules.cheeseRepository import CheeseRepository

#@repository chats
#@dbscheme (id, chat_name, last_activity, picture_id)
#@dbmodel Chat
class ChatRepository(CheeseRepository):

    #@query "select * from chats c where c.id = :chatId;"
    #@return one
    @staticmethod
    def findChatById(chatId):
        return CheeseRepository.findChatById([chatId])

    #@query "select c.id, chat_name, last_activity, c.picture_id from chats c
    #        inner join chats_t ct
    #            on ct.chat_id = c.id
    #        inner join users u
    #            on u.id = ct.user_id
    #        where u.id = :userId and c.last_activity <= :lastActivity
    #        order by c.last_activity desc
    #        limit :chatCount;"
    #@return array
    @staticmethod
    def findChatsFrom(userId, lastActivity, chatCount):
        return CheeseRepository.findChatsFrom([userId, lastActivity, chatCount])

    #@query "select case when exists
    #            (select * from users u1
    #            inner join chats_t ct1
    #                on u1.id = ct1.user_id
    #            inner join chats_t ct2
    #                on ct2.chat_id = ct1.chat_id
    #            inner join users u2
    #                on u2.id = ct2.user_id
    #            inner join chats c
    #                on c.id = ct2.chat_id
    #            where u1.id = :userId1 and u2.id = :userId2) 
    #        then cast(1 as bit)
    #        else cast(0 as bit) end;"
    #@return bool
    @staticmethod
    def doesChatExists(userId1, userId2):
        return CheeseRepository.doesChatExists([userId1, userId2])

    #@query "select count(*) from chats;"
    #@return num
    @staticmethod
    def findNewId():
        return CheeseRepository.findNewId([])

    #@query "select case when exists
    #                (select * from chats_t ct where ct.user_id = :userId and ct.chat_id = :chatId)
    #        then cast(1 as bit)
    #        else cast(0 as bit) end;"
    #@return bool
    @staticmethod
    def belongsToUserId(userId, chatId):
        return CheeseRepository.belongsToUserId([userId, chatId])

    #@query "select c.id, chat_name, last_activity, c.picture_id from chats c
    #            inner join chats_t ct
    #                on ct.chat_id = c.id
    #            inner join users u
    #                on u.id = ct.user_id
    #        where u.id = :userId;"
    #@return array
    @staticmethod
    def findChatsByUserId(userId):
        return CheeseRepository.findChatsByUserId([userId])

    #@query "select * from chats c where c.id in :ids;"
    #@return array
    @staticmethod
    def findChatsByIds(ids):
        return CheeseRepository.findChatsByIds([ids])

    @staticmethod
    def save(obj):
        return CheeseRepository.save([obj])

    @staticmethod
    def update(obj):
        return CheeseRepository.update([obj])


    
    
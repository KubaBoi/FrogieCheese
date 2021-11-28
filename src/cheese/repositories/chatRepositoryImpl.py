#!/usr/bin/env python
# -*- coding: utf-8 -*-
#AUTOGENERATED FILE

from cheese.databaseControll.database import Database
from python.models.Chat import Chat


class ChatRepositoryImpl:

    @staticmethod
    def init():
        ChatRepositoryImpl.table = "chats"
        ChatRepositoryImpl.scheme = "(id,chat_name,last_activity,picture_id)"
        ChatRepositoryImpl.schemeNoBrackets = "id,chat_name,last_activity,picture_id"

    @staticmethod
    def convert(var):
        try:
            var = int(var)
        except:
            var = var
        return var

    @staticmethod
    def toJson(object):
        scheme = ChatRepositoryImpl.schemeNoBrackets.split(",")
        ret = {}
        for s, o in zip(scheme, list(object)):
            try:
                ret[s] = int(o)
            except:
                ret[s] = o
        return ret

    @staticmethod
    def toModel(obj):
        model = Chat()
        model.id = ChatRepositoryImpl.convert(obj[0])
        model.chat_name = ChatRepositoryImpl.convert(obj[1])
        model.last_activity = ChatRepositoryImpl.convert(obj[2])
        model.picture_id = ChatRepositoryImpl.convert(obj[3])
        return model

    @staticmethod
    def fromModel(model):
        tuple = (
            model.id,
            model.chat_name,
            model.last_activity,
            model.picture_id
        )
        return tuple

    @staticmethod
    def findChatById(args):
        chatId = args[0]

        response = Database.query(f"select {ChatRepositoryImpl.schemeNoBrackets} from chats c where c.id = {chatId};")
        Database.done()
        if (response == None): return response
        if (len(response) > 0):
            return ChatRepositoryImpl.toModel(response[0])
        else: return None

    @staticmethod
    def findChatsFrom(args):
        userId = args[0]
        lastActivity = args[1]
        chatCount = args[2]

        response = Database.query(f"select c.id, chat_name, last_activity, c.picture_id from chats c inner join chats_t ct on ct.chat_id = c.id inner join users u on u.id = ct.user_id where u.id = {userId} and c.last_activity <= {lastActivity} order by c.last_activity desc limit {chatCount};")
        Database.done()
        if (response == None): return response
        resp = []
        for a in response:
            resp.append(ChatRepositoryImpl.toModel(a))
        return resp

    @staticmethod
    def doesChatExists(args):
        userId1 = args[0]
        userId2 = args[1]

        response = Database.query(f"select case when exists (select * from users u1 inner join chats_t ct1 on u1.id = ct1.user_id inner join chats_t ct2 on ct2.chat_id = ct1.chat_id inner join users u2 on u2.id = ct2.user_id inner join chats c on c.id = ct2.chat_id where u1.id = {userId1} and u2.id = {userId2}) then cast(1 as bit) else cast(0 as bit) end;")
        Database.done()
        if (response == None): return response
        if (response[0][0] == "1"): return True
        return False

    @staticmethod
    def findNewId(args):

        response = Database.query(f"select count(*) from chats;")
        Database.done()
        if (response == None): return response
        return int(response[0][0])

    @staticmethod
    def belongsToUserId(args):
        userId = args[0]
        chatId = args[1]

        response = Database.query(f"select case when exists (select * from chats_t ct where ct.user_id = {userId} and ct.chat_id = {chatId}) then cast(1 as bit) else cast(0 as bit) end;")
        Database.done()
        if (response == None): return response
        if (response[0][0] == "1"): return True
        return False

    @staticmethod
    def findChatsByUserId(args):
        userId = args[0]

        response = Database.query(f"select c.id, chat_name, last_activity, c.picture_id from chats c inner join chats_t ct on ct.chat_id = c.id inner join users u on u.id = ct.user_id where u.id = {userId};")
        Database.done()
        if (response == None): return response
        resp = []
        for a in response:
            resp.append(ChatRepositoryImpl.toModel(a))
        return resp

    @staticmethod
    def findChatsByIds(args):
        ids = args[0]

        response = Database.query(f"select {ChatRepositoryImpl.schemeNoBrackets} from chats c where c.id in {ids};")
        Database.done()
        if (response == None): return response
        resp = []
        for a in response:
            resp.append(ChatRepositoryImpl.toModel(a))
        return resp

    @staticmethod
    def save(args):
        obj = ChatRepositoryImpl.fromModel(args[0])

        try:
            Database.commit(f"insert into {ChatRepositoryImpl.table} {ChatRepositoryImpl.scheme} values {obj};")
            Database.done()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def update(args):
        obj = ChatRepositoryImpl.fromModel(args[0])

        try:
            Database.commit(f"update {ChatRepositoryImpl.table} set {ChatRepositoryImpl.scheme} = {obj} where id={obj[0]};")
            Database.done()
            return True
        except Exception as e:
            print(e)
            return False


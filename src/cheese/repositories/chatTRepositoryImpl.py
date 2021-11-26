#!/usr/bin/env python
# -*- coding: utf-8 -*-
#AUTOGENERATED FILE

from cheese.databaseControll.database import Database

class ChatTRepositoryImpl:

    @staticmethod
    def init():
        ChatTRepositoryImpl.table = "chats_t"
        ChatTRepositoryImpl.scheme = "(id,user_id,chat_id,last_delivered_message_id,last_seen_message_id)"
        ChatTRepositoryImpl.schemeNoBrackets = "id,user_id,chat_id,last_delivered_message_id,last_seen_message_id"

    @staticmethod
    def findChatTByUserIdAndChatId(args):
        userId = args[0]
        chatId = args[1]

        response = Database.query(f"select {ChatTRepositoryImpl.schemeNoBrackets} from chats_t ct where ct.user_id = {userId} and ct.chat_id = {chatId};")
        Database.done()
        if (len(response) > 0):
            return ChatTRepositoryImpl.toJson(response[0])
        else: return None

    @staticmethod
    def findChatsByUserID(args):
        userId = args[0]

        response = Database.query(f"select {ChatTRepositoryImpl.schemeNoBrackets} from chats_t ct where ct.user_id = {userId};")
        Database.done()
        resp = []
        for a in response:
            resp.append(ChatTRepositoryImpl.toJson(a[0]))
        return resp

    @staticmethod
    def findUndeliveredChatsByUserId(args):
        userId = args[0]

        response = Database.query(f"select ct.id, ct.user_id, ct.chat_id, ct.last_delivered_message_id, ct.last_seen_message_id from chats_t ct         where ct.user_id = {userId} and         (ct.last_delivered_message_id is NULL or         exists         (select ct2.id from chats_t ct2         inner join messages m         on m.id = ct2.last_delivered_message_id         where ct2.user_id = {userId} and exists         (select m2.id from messages m2         where m2.time_stamp > m.time_stamp and m2.chat_id = ct2.chat_id)));")
        Database.done()
        resp = []
        for a in response:
            resp.append(ChatTRepositoryImpl.toJson(a[0]))
        return resp

    @staticmethod
    def findNewId(args):

        response = Database.query(f"select count(*) from chats_t;")
        Database.done()
        return int(response[0][0])

    @staticmethod
    def findAllUsersFromChat(args):
        chatId = args[0]

        response = Database.query(f"select {ChatTRepositoryImpl.schemeNoBrackets} from chats_t ct where ct.chat_id = {chatId};")
        Database.done()
        resp = []
        for a in response:
            resp.append(ChatTRepositoryImpl.toJson(a[0]))
        return resp

    @staticmethod
    def save(args):
        obj = args[0]

        try:
            Database.commit(f"insert into {ChatTRepositoryImpl.table} {ChatTRepositoryImpl.scheme} values {obj};")
            Database.done()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def save(args):
        obj = args[0]

        try:
            Database.commit(f"update {ChatTRepositoryImpl.table} set ")
            Database.done()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def toJson(object):
        scheme = ChatTRepositoryImpl.schemeNoBrackets.split(",")
        ret = {}
        for s, o in zip(scheme, list(object)):
            try:
                ret[s] = int(o)
            except:
                ret[s] = o
        return ret


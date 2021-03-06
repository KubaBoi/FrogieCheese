#!/usr/bin/env python
# -*- coding: utf-8 -*-
#AUTOGENERATED FILE

from cheese.databaseControll.database import Database
from cheese.Logger import Logger
from python.models.ChatT import ChatT


class ChatTRepositoryImpl:

    @staticmethod
    def init():
        ChatTRepositoryImpl.table = "chats_t"
        ChatTRepositoryImpl.scheme = "(id,user_id,chat_id,last_delivered_message_id,last_seen_message_id)"
        ChatTRepositoryImpl.schemeNoBrackets = "id,user_id,chat_id,last_delivered_message_id,last_seen_message_id"

    @staticmethod
    def convert(var):
        if (type(var) is int):
            var = int(var)
        elif (type(var) is float):
            var = float(var)
        return var

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

    @staticmethod
    def toModel(obj):
        model = ChatT()
        model.id = ChatTRepositoryImpl.convert(obj[0])
        model.user_id = ChatTRepositoryImpl.convert(obj[1])
        model.chat_id = ChatTRepositoryImpl.convert(obj[2])
        model.last_delivered_message_id = ChatTRepositoryImpl.convert(obj[3])
        model.last_seen_message_id = ChatTRepositoryImpl.convert(obj[4])
        return model

    @staticmethod
    def fromModel(model):
        tuple = (
            model.id,
            model.user_id,
            model.chat_id,
            model.last_delivered_message_id,
            model.last_seen_message_id
        )
        return tuple

    @staticmethod
    def findChatTByUserIdAndChatId(args):
        userId = args[0]
        chatId = args[1]

        response = None
        try:
            db = Database()
            response = db.query(f"select {ChatTRepositoryImpl.schemeNoBrackets} from chats_t ct where ct.user_id = {userId} and ct.chat_id = {chatId};")
            db.done()
        except Exception as e:
            Logger.fail("An error occurred while query request", str(e))

        if (response == None): return response
        if (len(response) > 0):
            return ChatTRepositoryImpl.toModel(response[0])
        else: return None

    @staticmethod
    def findChatsByUserID(args):
        userId = args[0]

        response = None
        try:
            db = Database()
            response = db.query(f"select {ChatTRepositoryImpl.schemeNoBrackets} from chats_t ct where ct.user_id = {userId};")
            db.done()
        except Exception as e:
            Logger.fail("An error occurred while query request", str(e))

        if (response == None): return response
        resp = []
        for a in response:
            resp.append(ChatTRepositoryImpl.toModel(a))
        return resp

    @staticmethod
    def findUndeliveredChatsByUserId(args):
        userId = args[0]

        response = None
        try:
            db = Database()
            response = db.query(f"select ct.id, ct.user_id, ct.chat_id, ct.last_delivered_message_id, ct.last_seen_message_id from chats_t ct where ct.user_id = {userId} and (ct.last_delivered_message_id is NULL or exists (select ct2.id from chats_t ct2 inner join messages m on m.id = ct2.last_delivered_message_id where ct2.user_id = {userId} and exists (select m2.id from messages m2 where m2.time_stamp > m.time_stamp and m2.chat_id = ct2.chat_id)));")
            db.done()
        except Exception as e:
            Logger.fail("An error occurred while query request", str(e))

        if (response == None): return response
        resp = []
        for a in response:
            resp.append(ChatTRepositoryImpl.toModel(a))
        return resp

    @staticmethod
    def findNewId(args):

        response = None
        try:
            db = Database()
            response = db.query(f"select count(*) from chats_t;")
            db.done()
        except Exception as e:
            Logger.fail("An error occurred while query request", str(e))

        if (response == None): return response
        try: return int(response[0][0])
        except: return -1

    @staticmethod
    def findAllUsersFromChat(args):
        chatId = args[0]

        response = None
        try:
            db = Database()
            response = db.query(f"select {ChatTRepositoryImpl.schemeNoBrackets} from chats_t ct where ct.chat_id = {chatId};")
            db.done()
        except Exception as e:
            Logger.fail("An error occurred while query request", str(e))

        if (response == None): return response
        resp = []
        for a in response:
            resp.append(ChatTRepositoryImpl.toModel(a))
        return resp

    @staticmethod
    def findNewId(args):

        response = None
        try:
            db = Database()
            response = db.query(f"select max(id) from {ChatTRepositoryImpl.table};")
            db.done()
        except Exception as e:
            Logger.fail("An error occurred while query request", str(e))

        if (response == None): return response
        try: return int(response[0][0])
        except: return -1

    @staticmethod
    def save(args):
        obj = ChatTRepositoryImpl.fromModel(args[0])

        try:
            db = Database()
            db.commit(f"insert into {ChatTRepositoryImpl.table} {ChatTRepositoryImpl.scheme} values {obj};")
            db.done()
            return True
        except Exception as e:
            Logger.fail("An error occurred while commit request", str(e))
            return False

    @staticmethod
    def update(args):
        obj = ChatTRepositoryImpl.fromModel(args[0])

        try:
            db = Database()
            db.commit(f"update {ChatTRepositoryImpl.table} set {ChatTRepositoryImpl.scheme} = {obj} where id={obj[0]};")
            db.done()
            return True
        except Exception as e:
            Logger.fail("An error occurred while commit request", str(e))
            return False

    @staticmethod
    def delete(args):
        obj = ChatTRepositoryImpl.fromModel(args[0])

        try:
            db = Database()
            db.commit(f"delete from {ChatTRepositoryImpl.table} where id={obj[0]};")
            db.done()
            return True
        except Exception as e:
            Logger.fail("An error occurred while commit request", str(e))
            return False


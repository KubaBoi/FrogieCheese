#!/usr/bin/env python
# -*- coding: utf-8 -*-
#AUTOGENERATED FILE

from cheese.databaseControll.database import Database
from cheese.Logger import Logger
from python.models.Message import Message


class MessageRepositoryImpl:

    @staticmethod
    def init():
        MessageRepositoryImpl.table = "messages"
        MessageRepositoryImpl.scheme = "(id,author_id,content,chat_id,time_stamp)"
        MessageRepositoryImpl.schemeNoBrackets = "id,author_id,content,chat_id,time_stamp"

    @staticmethod
    def convert(var):
        try:
            var = int(var)
        except:
            var = var
        return var

    @staticmethod
    def toJson(object):
        scheme = MessageRepositoryImpl.schemeNoBrackets.split(",")
        ret = {}
        for s, o in zip(scheme, list(object)):
            try:
                ret[s] = int(o)
            except:
                ret[s] = o
        return ret

    @staticmethod
    def toModel(obj):
        model = Message()
        model.id = MessageRepositoryImpl.convert(obj[0])
        model.author_id = MessageRepositoryImpl.convert(obj[1])
        model.content = MessageRepositoryImpl.convert(obj[2])
        model.chat_id = MessageRepositoryImpl.convert(obj[3])
        model.time_stamp = MessageRepositoryImpl.convert(obj[4])
        return model

    @staticmethod
    def fromModel(model):
        tuple = (
            model.id,
            model.author_id,
            model.content,
            model.chat_id,
            model.time_stamp
        )
        return tuple

    @staticmethod
    def findMessagesFrom(args):
        chatId = args[0]
        timeStamp = args[1]
        messagesCount = args[2]

        response = None
        try:
            db = Database()
            response = db.query(f"select distinct m.id, author_id, content, m.chat_id, m.time_stamp from messages m inner join chats c on c.id = m.chat_id inner join chats_t ct on ct.chat_id = c.id inner join users u on u.id = ct.user_id where c.id = {chatId} and m.time_stamp <= {timeStamp} order by m.time_stamp desc limit {messagesCount};")
            db.done()
        except Exception as e:
            Logger.fail(str(e))

        if (response == None): return response
        resp = []
        for a in response:
            resp.append(MessageRepositoryImpl.toModel(a))
        return resp

    @staticmethod
    def findNewId(args):

        response = None
        try:
            db = Database()
            response = db.query(f"select count(*) from messages;")
            db.done()
        except Exception as e:
            Logger.fail(str(e))

        if (response == None): return response
        return int(response[0][0])

    @staticmethod
    def findById(args):
        messageId = args[0]

        response = None
        try:
            db = Database()
            response = db.query(f"select {MessageRepositoryImpl.schemeNoBrackets} from messages m where m.id = {messageId};")
            db.done()
        except Exception as e:
            Logger.fail(str(e))

        if (response == None): return response
        if (len(response) > 0):
            return MessageRepositoryImpl.toModel(response[0])
        else: return None

    @staticmethod
    def save(args):
        obj = MessageRepositoryImpl.fromModel(args[0])

        try:
            db = Database()
            db.commit(f"insert into {MessageRepositoryImpl.table} {MessageRepositoryImpl.scheme} values {obj};")
            db.done()
            return True
        except Exception as e:
            Logger.fail(str(e))
            return False

    @staticmethod
    def update(args):
        obj = MessageRepositoryImpl.fromModel(args[0])

        try:
            db = Database()
            db.commit(f"update {MessageRepositoryImpl.table} set {MessageRepositoryImpl.scheme} = {obj} where id={obj[0]};")
            db.done()
            return True
        except Exception as e:
            Logger.fail(str(e))
            return False

    @staticmethod
    def delete(args):
        obj = MessageRepositoryImpl.fromModel(args[0])

        try:
            db = Database()
            db.commit(f"delete from {MessageRepositoryImpl.table} where id={obj[0]};")
            db.done()
            return True
        except Exception as e:
            Logger.fail(str(e))
            return False


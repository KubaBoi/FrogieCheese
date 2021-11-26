#!/usr/bin/env python
# -*- coding: utf-8 -*-
#AUTOGENERATED FILE

from cheese.databaseControll.database import Database

class MessageRepositoryImpl:

    @staticmethod
    def init():
        MessageRepositoryImpl.table = "messages"
        MessageRepositoryImpl.scheme = "(id,author_id,content,chat_id,time_stamp)"
        MessageRepositoryImpl.schemeNoBrackets = "id,author_id,content,chat_id,time_stamp"

    @staticmethod
    def findMessagesFrom(args):
        chatId = args[0]
        timeStamp = args[1]
        messagesCount = args[2]

        response = Database.query(f"select distinct m.id, author_id, content, m.chat_id, m.time_stamp from messages m                 inner join chats c                 on c.id = m.chat_id                 inner join chats_t ct                 on ct.chat_id = c.id                 inner join users u                 on u.id = ct.user_id                 where c.id = {chatId} and m.time_stamp <= {timeStamp}                 order by m.time_stamp desc                 limit {messagesCount};")
        Database.done()
        resp = []
        for a in response:
            resp.append(MessageRepositoryImpl.toJson(a))
        return resp

    @staticmethod
    def findNewId(args):

        response = Database.query(f"select count(*) from messages;")
        Database.done()
        return int(response[0][0])

    @staticmethod
    def findById(args):
        messageId = args[0]

        response = Database.query(f"select {MessageRepositoryImpl.schemeNoBrackets} from messages m where m.id = {messageId};")
        Database.done()
        if (len(response) > 0):
            return MessageRepositoryImpl.toJson(response[0])
        else: return None

    @staticmethod
    def save(args):
        obj = args[0]

        try:
            Database.commit(f"insert into {MessageRepositoryImpl.table} {MessageRepositoryImpl.scheme} values {obj};")
            Database.done()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def update(args):
        obj = args[0]

        try:
            Database.commit(f"update {MessageRepositoryImpl.table} set {MessageRepositoryImpl.scheme} = {obj} where id={obj[0]};")
            Database.done()
            return True
        except Exception as e:
            print(e)
            return False

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


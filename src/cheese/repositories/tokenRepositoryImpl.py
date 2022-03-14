#!/usr/bin/env python
# -*- coding: utf-8 -*-
#AUTOGENERATED FILE

from cheese.databaseControll.database import Database
from cheese.Logger import Logger
from python.models.Token import Token


class TokenRepositoryImpl:

    @staticmethod
    def init():
        TokenRepositoryImpl.table = "tokens"
        TokenRepositoryImpl.scheme = "(id,token,user_id,ip,end_time)"
        TokenRepositoryImpl.schemeNoBrackets = "id,token,user_id,ip,end_time"

    @staticmethod
    def convert(var):
        try:
            var = int(var)
        except:
            var = var
        return var

    @staticmethod
    def toJson(object):
        scheme = TokenRepositoryImpl.schemeNoBrackets.split(",")
        ret = {}
        for s, o in zip(scheme, list(object)):
            try:
                ret[s] = int(o)
            except:
                ret[s] = o
        return ret

    @staticmethod
    def toModel(obj):
        model = Token()
        model.id = TokenRepositoryImpl.convert(obj[0])
        model.token = TokenRepositoryImpl.convert(obj[1])
        model.user_id = TokenRepositoryImpl.convert(obj[2])
        model.ip = TokenRepositoryImpl.convert(obj[3])
        model.end_time = TokenRepositoryImpl.convert(obj[4])
        return model

    @staticmethod
    def fromModel(model):
        tuple = (
            model.id,
            model.token,
            model.user_id,
            model.ip,
            model.end_time
        )
        return tuple

    @staticmethod
    def findTokenByIdAndIpAndActive(args):
        userId = args[0]
        ip = args[1]
        time = args[2]

        response = None
        try:
            db = Database()
            response = db.query(f"select {TokenRepositoryImpl.schemeNoBrackets} from tokens t where t.user_id = {userId} and t.ip = {ip} and t.end_time >= {time};")
            db.done()
        except Exception as e:
            Logger.fail(str(e))

        if (response == None): return response
        if (len(response) > 0):
            return TokenRepositoryImpl.toModel(response[0])
        else: return None

    @staticmethod
    def findToken(args):
        token = args[0]
        ip = args[1]
        time = args[2]

        response = None
        try:
            db = Database()
            response = db.query(f"select {TokenRepositoryImpl.schemeNoBrackets} from tokens t where t.token = {token} and t.ip = {ip} and t.end_time >= {time};")
            db.done()
        except Exception as e:
            Logger.fail(str(e))

        if (response == None): return response
        if (len(response) > 0):
            return TokenRepositoryImpl.toModel(response[0])
        else: return None

    @staticmethod
    def validateTokenUnique(args):
        token = args[0]

        response = None
        try:
            db = Database()
            response = db.query(f"select case when exists (select * from tokens t where t.token = {token}) then cast(0 as bit) else cast(1 as bit) end;")
            db.done()
        except Exception as e:
            Logger.fail(str(e))

        if (response == None): return response
        if (response[0][0] == "1"): return True
        return False

    @staticmethod
    def authorizeYourselfByToken(args):
        token = args[0]
        ip = args[1]
        time = args[2]

        response = None
        try:
            db = Database()
            response = db.query(f"select case when exists (select * from tokens t where t.token = {token} and t.ip = {ip} and t.end_time >= {time}) then cast(1 as bit) else cast(0 as bit) end;")
            db.done()
        except Exception as e:
            Logger.fail(str(e))

        if (response == None): return response
        if (response[0][0] == "1"): return True
        return False

    @staticmethod
    def findNewId(args):

        response = None
        try:
            db = Database()
            response = db.query(f"select count(*) from tokens;")
            db.done()
        except Exception as e:
            Logger.fail(str(e))

        if (response == None): return response
        return int(response[0][0])

    @staticmethod
    def save(args):
        obj = TokenRepositoryImpl.fromModel(args[0])

        try:
            db = Database()
            db.commit(f"insert into {TokenRepositoryImpl.table} {TokenRepositoryImpl.scheme} values {obj};")
            db.done()
            return True
        except Exception as e:
            Logger.fail(str(e))
            return False

    @staticmethod
    def update(args):
        obj = TokenRepositoryImpl.fromModel(args[0])

        try:
            db = Database()
            db.commit(f"update {TokenRepositoryImpl.table} set {TokenRepositoryImpl.scheme} = {obj} where id={obj[0]};")
            db.done()
            return True
        except Exception as e:
            Logger.fail(str(e))
            return False

    @staticmethod
    def delete(args):
        obj = TokenRepositoryImpl.fromModel(args[0])

        try:
            db = Database()
            db.commit(f"delete from {TokenRepositoryImpl.table} where id={obj[0]};")
            db.done()
            return True
        except Exception as e:
            Logger.fail(str(e))
            return False


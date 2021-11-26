#!/usr/bin/env python
# -*- coding: utf-8 -*-
#AUTOGENERATED FILE

from cheese.databaseControll.database import Database

class UserRepositoryImpl:

    @staticmethod
    def init():
        UserRepositoryImpl.table = "users"
        UserRepositoryImpl.scheme = "(id,user_name,email,picture_id)"
        UserRepositoryImpl.schemeNoBrackets = "id,user_name,email,picture_id"

    @staticmethod
    def findUserByCredentials(args):
        userName = args[0]
        password = args[1]
        duration = args[2]

        response = Database.query(f"select u.id, u.email, u.user_name, u.picture_id from passwords p         inner join users u         on u.id = p.user_id         where p.password = {password} and p.duration > {duration} and u.user_name = {userName};")
        Database.done()
        if (len(response) > 0):
            return UserRepositoryImpl.toJson(response[0])
        else: return None

    @staticmethod
    def findUserByName(args):
        userName = args[0]

        response = Database.query(f"select {UserRepositoryImpl.schemeNoBrackets} from users u where u.user_name = {userName};")
        Database.done()
        if (len(response) > 0):
            return UserRepositoryImpl.toJson(response[0])
        else: return None

    @staticmethod
    def findUserById(args):
        userId = args[0]

        response = Database.query(f"select {UserRepositoryImpl.schemeNoBrackets} from users u where u.id = {userId};")
        Database.done()
        if (len(response) > 0):
            return UserRepositoryImpl.toJson(response[0])
        else: return None

    @staticmethod
    def validateUserName(args):
        userName = args[0]

        response = Database.query(f"select case when exists         (select * from users u where u.user_name = {userName})         then cast(0 as bit)         else cast(1 as bit) end;")
        Database.done()
        if (response[0][0] == "1"): return True
        return False

    @staticmethod
    def findNewId(args):

        response = Database.query(f"select count(*) from users;")
        Database.done()
        return int(response[0][0])

    @staticmethod
    def findUserByIpAndToken(args):
        ip = args[0]
        token = args[1]

        response = Database.query(f"select u.id, u.user_name, u.picture_id, u.email from users u         inner join tokens t         on t.user_id = u.id         where t.token = {token} and t.ip = {ip};")
        Database.done()
        if (len(response) > 0):
            return UserRepositoryImpl.toJson(response[0])
        else: return None

    @staticmethod
    def findUsersDynamic(args):
        userNameStart = args[0]

        response = Database.query(f"select {UserRepositoryImpl.schemeNoBrackets} from users u where LOWER(u.user_name) like {userNameStart}%")
        Database.done()
        resp = []
        for a in response:
            resp.append(UserRepositoryImpl.toJson(a[0]))
        return resp

    @staticmethod
    def save(args):
        obj = args[0]

        try:
            Database.commit(f"insert into {UserRepositoryImpl.table} {UserRepositoryImpl.scheme} values {obj};")
            Database.done()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def save(args):
        obj = args[0]

        try:
            Database.commit(f"update {UserRepositoryImpl.table} set ")
            Database.done()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def toJson(object):
        scheme = UserRepositoryImpl.schemeNoBrackets.split(",")
        ret = {}
        for s, o in zip(scheme, list(object)):
            try:
                ret[s] = int(o)
            except:
                ret[s] = o
        return ret


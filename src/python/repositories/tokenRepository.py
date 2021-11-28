#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cheese.modules.cheeseRepository import CheeseRepository

#@repository tokens
#@dbscheme (id, token, user_id, ip, end_time)
#@dbmodel Token
class TokenRepository(CheeseRepository):

    #@query "select * from tokens t where
    #       t.user_id = :userId and
    #       t.ip = :ip and
    #       t.end_time >= :time;"
    #@return one
    @staticmethod
    def findTokenByIdAndIpAndActive(userId, ip, time):
        return CheeseRepository.findTokenByIdAndIpAndActive([userId, ip, time])

    
    #@query "select * from tokens t where
    #        t.token = :token and
    #        t.ip = :ip and
    #        t.end_time >= :time;"
    #@return one
    @staticmethod
    def findToken(token, ip, time):
        return CheeseRepository.findToken([token, ip, time])


    #@query "select case when exists
    #       (select * from tokens t where t.token = :token)
    #       then cast(0 as bit)
    #       else cast(1 as bit) end;"
    #@return bool
    @staticmethod
    def validateTokenUnique(token):
        return CheeseRepository.validateTokenUnique([token])


    #@query "select case when exists
    #       (select * from tokens t where
    #       t.token = :token and
    #       t.ip = :ip and
    #       t.end_time >= :time)
    #       then cast(1 as bit)
    #       else cast(0 as bit) end;"
    #@return bool
    @staticmethod
    def authorizeYourselfByToken(token, ip, time):
        return CheeseRepository.authorizeYourselfByToken([token, ip, time])

    #@query "select count(*) from tokens;"
    #@return num
    @staticmethod
    def findNewId():
        return CheeseRepository.findNewId([])

    @staticmethod
    def save(obj):
        return CheeseRepository.save([obj])

    @staticmethod
    def update(obj):
        return CheeseRepository.update([obj])

    
    
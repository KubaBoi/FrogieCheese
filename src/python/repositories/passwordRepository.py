#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cheese.modules.cheeseRepository import CheeseRepository

#@repository passwords
#@dbscheme (id, user_id, password, duration)
#@dbmodel Password
class PasswordRepository(CheeseRepository):

    #@query "select case when exists
    #        (select * from passwords p where p.user_id = :userId)
    #        then cast(1 as bit)
    #        else cast(0 as bit) end;"
    #@return bool
    @staticmethod
    def findValidPassword(userId):
        return CheeseRepository.findValidPassword([userId])

    #@query "select count(*) from passwords;"
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

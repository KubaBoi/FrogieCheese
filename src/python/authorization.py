#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.parse import unquote

from cheese.modules.cheeseController import CheeseController
from cheese.ErrorCodes import Error

from python.repositories.tokenRepository import TokenRepository
from python.repositories.userRepository import UserRepository

#@authorization enabled
class Authorization:

    @staticmethod
    def authorize(server, path, method):
        if (path.startswith("/authentication/login")):
            return None
        else:
            token = Authorization.getToken(server)
            if (Authorization.authorizeByToken(server, token)):
                ip = CheeseController.getClientAddress(server)
                return {
                    "user": UserRepository.findUserByIpAndToken(ip, token),
                    "token": token,
                    "ip": ip
                }
            
            CheeseController.sendResponse(server, Error.BadToken)
            return None


    @staticmethod
    def getToken(server):
        args = CheeseController.readArgs(server)
        # bad json
        if (not CheeseController.validateJson(["TOKEN"], args)):
            CheeseController.sendResponse(server, Error.BadJson)
            return None

        return args["TOKEN"]

    @staticmethod
    def authorizeByToken(server, token):
        return TokenRepository.authorizeYourselfByToken(token, CheeseController.getClientAddress(server), CheeseController.getTime())
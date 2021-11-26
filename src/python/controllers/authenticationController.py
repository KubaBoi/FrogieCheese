#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import random

from cheese.modules.cheeseController import CheeseController
from cheese.ErrorCodes import Error

from python.repositories.userRepository import UserRepository
from python.repositories.passwordRepository import PasswordRepository
from python.repositories.tokenRepository import TokenRepository

#@controller /authentication
class AuthenticationController(CheeseController):

    @staticmethod
    def init():
        AuthenticationController.TOKEN_LENGTH = 20
        AuthenticationController.TOKEN_DURATION = 3600 # 1 hour

    #@post /login
    @staticmethod
    def login(server, path, auth):
        args = CheeseController.readArgs(server)

        # bad json
        if (not CheeseController.validateJson(["USER_NAME", "PASSWORD"], args)):
            CheeseController.sendResponse(server, Error.BadJson)
            return

        userName = args["USER_NAME"]
        password = args["PASSWORD"]
        ip = CheeseController.getClientAddress(server)

        # password check
        user = UserRepository.findUserByCredentials(userName, password, CheeseController.getTime())
        if (user == None):
            user = UserRepository.findUserByName(userName)
            if (user != None):
                if (PasswordRepository.findValidPassword(user["id"])):
                    CheeseController.sendResponse(server, Error.OldPass)
                    return
            CheeseController.sendResponse(server, Error.BadCred)
            return

        # OK
        token = AuthenticationController.generateToken(user["id"], ip)

        response = CheeseController.createResponse(
            {
                "USER": user,
                "TOKEN": token
            }, 200
        )

        CheeseController.sendResponse(server, response)


    #@post /getUserByToken
    @staticmethod
    def getUserByToken(server, path, auth):
        if (auth == None):
            return
        token = auth["token"]
        ip = auth["ip"]

        user = UserRepository.findUserByIpAndToken(ip, token)
        
        response = CheeseController.createResponse({"USER": user}, 200)

        CheeseController.sendResponse(server, response)



    #METHODS

    @staticmethod
    def generateToken(userId, ip):
        token = TokenRepository.findTokenByIdAndIpAndActive(userId, ip, CheeseController.getTime())

        if (token == None):

            token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(AuthenticationController.TOKEN_LENGTH))
            while (not TokenRepository.validateTokenUnique(token)):
                token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(AuthenticationController.TOKEN_LENGTH))
            TokenRepository.save((token, userId, ip, CheeseController.getTime(AuthenticationController.TOKEN_DURATION)))
            return token
        return token["token"]


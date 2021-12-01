#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from pathlib import Path

from http.server import HTTPServer
from cheese.Logger import Logger

from cheese.resourceManager import ResMan
from cheese.appSettings import Settings
from cheese.server.cheeseServer import CheeseServer
from cheese.databaseControll.database import Database
from cheese.modules.cheeseRepository import CheeseRepository
from cheese.ErrorCodes import Error
"""
File generated by Cheese Framework

initialize Cheese Application
"""

class Cheese:

    @staticmethod
    def init():
        # initialization of root directory
        ResMan.setPath(Path(__file__).parent.parent.parent)
        Cheese.printInit()

        # init errors
        Error.init()

        # loads application settings
        Settings.loadSettings()

        # connect to database
        Database.connect()

        #initialization of repositories
        CheeseRepository.initRepositories()

        # initialization of server
        Cheese.initServer()

    # initialization application server
    @staticmethod
    def initServer():
        Cheese.server = HTTPServer((Settings.host, Settings.port), CheeseServer)

    # start server
    @staticmethod
    def serveForever():
        Logger.info(f"Server Starts - {Settings.host}:{Settings.port}")
        try:
            Cheese.server.serve_forever()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            Logger.fail(str(e))
        Logger.info(f"Server Stops - {Settings.host}:{Settings.port}")

    # init print
    @staticmethod
    def printInit():
        Logger.info(10*"=")
        with open(f"{ResMan.cheese()}/initString.txt", "r") as f:
            print(f.read())


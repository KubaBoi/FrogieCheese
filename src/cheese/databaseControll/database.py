#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2

from cheese.appSettings import Settings
from cheese.Logger import Logger

"""
File generated by Cheese Framework

database connection of Cheese Application
"""

class Database:

    # connect to database
    @staticmethod
    def connect():
        Database.connection = psycopg2.connect(
                host=Settings.dbHost,
                database=Settings.dbName,
                user=Settings.dbUser,
                password=Settings.dbPassword,
                port=Settings.dbPort)

        Database.cursor = Database.connection.cursor()
        Logger.okBlue(f"CONNECTED TO {Settings.dbHost}:{Settings.dbPort} {Settings.dbName}")

    # close connection with database
    @staticmethod
    def close():
        Database.cursor.close()
        Logger.okBlue(f"CONNECTION TO {Settings.dbHost}:{Settings.dbPort} {Settings.dbName} CLOSED")

    # select query
    @staticmethod
    def query(sql):
        Logger.okBlue(Logger.WARNING + "QUERY: " + Logger.ENDC + sql)
        try:
            Database.cursor.execute(sql)
        except:
            Database.rollback()
            return None
        return Database.cursor.fetchall()

    # insert, update ...
    @staticmethod
    def commit(sql):
        Logger.okBlue(Logger.WARNING + "COMMIT: " + Logger.ENDC + sql)
        try:
            Database.cursor.execute(sql)
        except:
            Database.rollback()

    # commit when done
    @staticmethod
    def done():
        Database.connection.commit()

    @staticmethod
    def rollback():
        Database.connection.rollback()
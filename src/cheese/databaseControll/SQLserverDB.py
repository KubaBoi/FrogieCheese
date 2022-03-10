#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyodbc 

from cheese.appSettings import Settings
from cheese.Logger import Logger

"""
File generated by Cheese Framework

database connection of Cheese Application for SQL Server
"""

class SQLServerDB:

    # connect to database
    def connect(self):
        self.connection = pyodbc.connect(f"Driver={Settings.dbDriver};"
                      f"Server={Settings.dbHost},{Settings.dbPort};"
                      f"Database={Settings.dbName};"
                      f"UID={Settings.dbUser};"
                      f"PWD={Settings.dbPassword};"
                      f"Trusted_Connection=yes;")

        #self.cursor = self.connection.cursor()
        Logger.okBlue(f"CONNECTED TO {Settings.dbHost}:{Settings.dbPort} {Settings.dbName}")

    # close connection with database
    def close(self):
        self.cursor.close()
        Logger.okBlue(f"CONNECTION TO {Settings.dbHost}:{Settings.dbPort} {Settings.dbName} CLOSED")

    # select query
    def query(self, sql):
        self.cursor = self.connection.cursor()
        Logger.okBlue(Logger.WARNING + "QUERY: " + Logger.ENDC + sql)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            Logger.fail(str(e))
            self.rollback()
            return None
        ret = self.cursor.fetchall()
        self.cursor.close()
        return ret

    # insert, update ...
    def commit(self, sql):
        if (Settings.canCommit):
            self.cursor = self.connection.cursor()
            Logger.okBlue(Logger.WARNING + "COMMIT: " + Logger.ENDC + sql)
            try:
                self.cursor.execute(sql)
            except Exception as e:
                Logger.fail(str(e))
                self.rollback()
            self.cursor.close()
        else:
            Logger.fail("Commiting is not allowed")

    # commit when done
    def done(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
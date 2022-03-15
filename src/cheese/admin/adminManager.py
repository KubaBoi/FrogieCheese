
import os
import json
import time
import sys
import subprocess

from cheese.modules.cheeseController import CheeseController
from cheese.Logger import Logger
from cheese.resourceManager import ResMan
from cheese.appSettings import Settings
from cheese.ErrorCodes import Error

class AdminManager:

    @staticmethod
    def controller(server):
        if (not AdminManager.authorizeAsAdmin(server)):
            AdminManager.__sendFile(server, "/admin/login.html")
            return

        if (server.path == "/admin"):
            AdminManager.__sendFile(server, "/admin/index.html") 
            return
        elif (server.path == "/admin/createUser"): #TODO
            AdminManager.__createUser(server)
            return
        elif (server.path.startswith("/admin/logs")):
            AdminManager.__showLogs(server)
            return 
        elif (server.path == "/admin/getSettings"):
            AdminManager.__getSettings(server)
            return
        elif (server.path == "/admin/getActiveLog"):
            AdminManager.__getActiveLog(server)
            return
        elif (server.path == "/admin/restart"):
            AdminManager.__restartServer(server)
            return
        elif (server.path == "/admin/shutdown"):
            AdminManager.__shutDown(server)
            return
        AdminManager.__sendFile(server, server.path)        
        

    @staticmethod
    def authorizeAsAdmin(server):
        cookies = CheeseController.getCookies(server)
        if (not CheeseController.validateJson(["adminName", "adminPass"], cookies)):
            return False
        for user in Settings.adminSettings["adminUsers"]:
            if (user["name"] == cookies["adminName"] and
                user["password"] == cookies["adminPass"]):
                return True
        return False


    # PRIVATE METHODS

    @staticmethod
    def __sendFile(server, file):
        file = ResMan.joinPath(ResMan.cheese(), file)
        if (not os.path.exists(file)):
            with open(f"{ResMan.error()}/error404.html", "rb") as f:
                CheeseController.sendResponse(server, (f.read(), 404))
            return

        with open(f"{file}", "r", encoding="utf-8") as f:
            CheeseController.sendResponse(server, (bytes(f.read(), "utf-8"), 200), "text/html")

    @staticmethod
    def __createUser(server):
        pass

    @staticmethod
    def __showLogs(server):
        CheeseController.sendResponse(server, Logger.serveLogs(server), "text/html")

    @staticmethod
    def __getSettings(server):
        js = Settings.loadJson()
        CheeseController.sendResponse(server, (bytes(json.dumps(js), "utf-8"), 200), "text/html")

    @staticmethod
    def __getActiveLog(server):
        for root, dirs, files in os.walk(ResMan.logs()):
            activeLog = sorted(files)[-1]
        
        log = ResMan.joinPath(ResMan.logs(), activeLog)
        with open(f"{log}", "r") as f:
            lines = f.readlines()
            min = 0
            if (len(lines) >= 1000): min = len(lines) - 1000
            onlyTable = "".join(lines[min:(min+1000)])
        response = CheeseController.createResponse({"RESPONSE": {"LOG_DESC": activeLog, "LOG": onlyTable}}, 200)
        CheeseController.sendResponse(server, response, "text/html")

    @staticmethod
    def __restartServer(server):
        Logger.warning(20*"=")
        Logger.warning("REQUEST FOR SERVER RESTART SUCCESSFULLY RECIEVED", silence=False)
        Logger.warning("Restart will start in 5 seconds", silence=False)
        time.sleep(5)
        for root, dirs, files in os.walk(ResMan.src()):
            server.server.socket.close()
            time.sleep(5)
            if (os.name == "nt"):
                subprocess.call(f"{sys.executable} \"{ResMan.joinPath(ResMan.src(), files[0])}\"")
            else:
                subprocess.call(f"{sys.executable} \"{ResMan.joinPath(ResMan.src(), files[0])}\"", shell=True)

    @staticmethod
    def __shutDown(server):
        Logger.warning(20*"=")
        Logger.warning("REQUEST FOR SERVER SHUT DOWN SUCCESSFULLY RECIEVED", header=False, silence=False)
        Logger.warning("Shut down will start in 5 seconds", header=False, silence=False)
        time.sleep(5)
        server.server.socket.close()
        
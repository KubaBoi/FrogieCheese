import inspect
import os
import logging

from traceback import format_exc
from datetime import datetime

from cheese.resourceManager import ResMan
from cheese.appSettings import Settings

class FileFilter(logging.Filter):
    def filter(self, rec):
        if (rec.levelno == logging.FILE):
            rec.msg = rec.msg.replace(Logger.HEADER, "")
            rec.msg = rec.msg.replace(Logger.OKBLUE, "")
            rec.msg = rec.msg.replace(Logger.OKCYAN, "")
            rec.msg = rec.msg.replace(Logger.OKGREEN, "")
            rec.msg = rec.msg.replace(Logger.WARNING, "")
            rec.msg = rec.msg.replace(Logger.FAIL, "")
            rec.msg = rec.msg.replace(Logger.ENDC, "")
            rec.msg = rec.msg.replace(Logger.BOLD, "")
            rec.msg = rec.msg.replace(Logger.UNDERLINE, "")
            return True
        return False

class HtmlFilter(logging.Filter):
    def filter(self, rec):
        if (rec.levelno == logging.HTML_FILE):
            rec.msg = rec.msg.replace(Logger.HEADER, "<label style='font-weight:bold;'>")
            rec.msg = rec.msg.replace(Logger.OKBLUE, "<label style='color:#4542fc;'>")
            rec.msg = rec.msg.replace(Logger.OKCYAN, "<label style='color:#0ff;'>")
            rec.msg = rec.msg.replace(Logger.OKGREEN, "<label style='color:#0f0;'>")
            rec.msg = rec.msg.replace(Logger.WARNING, "<label style='color:#ff0;'>")
            rec.msg = rec.msg.replace(Logger.FAIL, "<label style='color:#f00;'>")
            rec.msg = rec.msg.replace(Logger.ENDC, "</label>")
            rec.msg = rec.msg.replace(Logger.BOLD, "<label style='font-weight:bold;'>")
            rec.msg = rec.msg.replace(Logger.UNDERLINE, "<label style='text-decoration:underline;'>")
            return True
        return False

class ConsoleFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno == logging.CONSOLE

class Logger:

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def initLogger():
        Logger.__addLoggingLevel("HTML_FILE", 11)
        Logger.__addLoggingLevel("FILE", 10)
        Logger.__addLoggingLevel("CONSOLE", 9)

        logFormatter = logging.Formatter(fmt="%(asctime)s - %(message)s", datefmt="%H:%M:%S")
        htmlFormatter = logging.Formatter(fmt="<tr><td>%(asctime)s</td><td>%(message)s</td></tr>", datefmt="%H:%M:%S")
        rootLogger = logging.getLogger()

        date = datetime.now()
        fileHandler = logging.FileHandler(ResMan.joinPath(ResMan.logs(), f"log{date.strftime('%Y-%m-%d-%H-%M-%S')}.log"), mode="w")
        fileHandler.setFormatter(logFormatter)
        fileHandler.addFilter(FileFilter())
        rootLogger.addHandler(fileHandler)

        htmlHandler = logging.FileHandler(ResMan.joinPath(ResMan.logs(), f"log{date.strftime('%Y-%m-%d-%H-%M-%S')}.html"), mode="a")
        htmlHandler.setFormatter(htmlFormatter)
        htmlHandler.addFilter(HtmlFilter())
        rootLogger.addHandler(htmlHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        consoleHandler.addFilter(ConsoleFilter())
        rootLogger.addHandler(consoleHandler)

        rootLogger.setLevel(logging.CONSOLE)

        with open(ResMan.joinPath(ResMan.logs(), f"log{date.strftime('%Y-%m-%d-%H-%M-%S')}.html"), "a") as f:
            f.write("<!DOCTYPE html>\n<html style='scroll-behavior:smooth;'>\n<head>\n<title>Cheese Logs</title>\n<meta charset='utf-8'>\n")
            f.write("<link rel='icon' href='data:;base64,iVBORw0KGgo='>\n")
            f.write("</head><body style='color:#fff;background-color:#2b2b2b;font-family: Arial, Helvetica, sans-serif;'>\n")
            f.write("<div style='position:fixed;right:50px;top:5px;'>");
            f.write("<input type='checkbox' id='aS' checked><lable>Autoscroll</label><br>")
            f.write("<input type='checkbox' id='aR' checked><lable>Autoreload</label></div>")
            f.write("<script src='/logs/logJSscript.js'></script>")
            f.write("<script>run();</script>")
            f.write(f"<h1>Cheese log - {date.strftime('%Y-%m-%d-%H-%M-%S')}</h1>\n")
            f.write("<table style='margin-bottom:100px;'>\n")

    
    @staticmethod
    def info(message, allowHeader=True, silence=True):
        if (allowHeader): header = Logger.__getMethod()
        else: header = ""
        logging.file(header + message)
        message = Logger.__infoPrint(message, header)
        logging.html_file(message)
        if (Settings.allowDebug or not silence):
            logging.console(message)

    @staticmethod
    def okBlue(message, allowHeader=True, silence=True):
        if (allowHeader): header = Logger.__getMethod()
        else: header = ""
        logging.file(header + message)
        message = Logger.__okBluePrint(message, header)
        logging.html_file(message)
        if (Settings.allowDebug or not silence):
            logging.console(message)

    @staticmethod
    def okCyan(message, allowHeader=True, silence=True):
        if (allowHeader): header = Logger.__getMethod()
        else: header = ""
        logging.file(header + message)
        message = Logger.__okCyanPrint(message, header)
        logging.html_file(message)
        if (Settings.allowDebug or not silence):
            logging.console(message)

    @staticmethod
    def okGreen(message, allowHeader=True, silence=True):
        if (allowHeader): header = Logger.__getMethod()
        else: header = ""
        logging.file(header + message)
        message = Logger.__okGreenPrint(message, header)
        logging.html_file(message)
        if (Settings.allowDebug or not silence):
            logging.console(message)

    @staticmethod
    def warning(message, allowHeader=True, silence=True):
        if (allowHeader): header = Logger.__getMethod()
        else: header = ""
        logging.file(header + message)
        message = Logger.__warningPrint(message, header)
        logging.html_file(message)
        if (Settings.allowDebug or not silence):
            logging.console(message)

    @staticmethod
    def fail(message, e, allowHeader=True, silence=True):
        if (allowHeader): header = Logger.__getMethod()
        else: header = ""
        message = f"{message}\n{20*'='}\n{repr(e)}\n{format_exc()}\n{10*'='}"
        logging.file(header + message)
        message = Logger.__failPrint(message, header)
        logging.html_file(message)
        if (Settings.allowDebug or not silence):
            logging.console(message)

    @staticmethod
    def bold(message, allowHeader=True, silence=True):
        if (allowHeader): header = Logger.__getMethod()
        else: header = ""
        logging.file(header + message)
        message = Logger.__boldPrint(message, header)
        logging.html_file(message)
        if (Settings.allowDebug or not silence):
            logging.console(message)

    @staticmethod
    def underline(message, allowHeader=True, silence=True):
        if (allowHeader): header = Logger.__getMethod()
        else: header = ""
        logging.file(header + message)
        message = Logger.__underlinePrint(message, header)
        logging.html_file(message)
        if (Settings.allowDebug or not silence):
            logging.console(message)

    @staticmethod
    def listLogs():
        for root, dirs, files in os.walk(ResMan.logs()):
            response = "<!DOCTYPE html>\n<html>\n<head>\n<title>Cheese Logs</title>\n<meta charset='utf-8'>"
            response += "<style>a{color:#4542fc;} a:visited{color:red;}</style></head>\n"
            response += "<body style='color:#fff;background-color:#2b2b2b;font-family: Arial, Helvetica, sans-serif;'>"
            response += "<h1>Cheese Logs</h1><table>"
            for name in files:
                if (not name.endswith(".log")): continue
                response += f"<tr><td><a href='/logs/{name.replace('.log', '.html')}'>"
                response += f"{name.replace('.log', '.html')}</a></td>"
                response += f"<td>{os.path.getsize(ResMan.joinPath(ResMan.logs(), name))}</td></tr>"
            response += "</table></body></html>"
        return (bytes(response, "utf-8"), 200)

    @staticmethod
    def serveLogs(server):
        path = server.path
        if (path == "/logs" or path == "/logs/"):
            logging.file(f"listing log files: {server.client_address[0]}")
            return Logger.listLogs()

        log = ResMan.joinPath(ResMan.root(), path)
        logging.file(f"Serving log file: {server.client_address[0]} \"{server.path}\"")
        
        if (not os.path.exists(f"{log}")):
            with open(f"{ResMan.error()}/error404.html", "rb") as f:
                return (f.read(), 404)

        with open(f"{log}", "rb") as f:
            return (f.read(), 200)
                

    #PRIVATE METHODS

    @staticmethod
    def __addLoggingLevel(levelName, levelNum, methodName=None):
        if not methodName:
            methodName = levelName.lower()

        if hasattr(logging, levelName):
            raise AttributeError('{} already defined in logging module'.format(levelName))
        if hasattr(logging, methodName):
            raise AttributeError('{} already defined in logging module'.format(methodName))
        if hasattr(logging.getLoggerClass(), methodName):
            raise AttributeError('{} already defined in logger class'.format(methodName))

        def logForLevel(self, message, *args, **kwargs):
            if self.isEnabledFor(levelNum):
                self._log(levelNum, message, args, **kwargs)
        def logToRoot(message, *args, **kwargs):
            logging.log(levelNum, message, *args, **kwargs)

        logging.addLevelName(levelNum, levelName)
        setattr(logging, levelName, levelNum)
        setattr(logging.getLoggerClass(), methodName, logForLevel)
        setattr(logging, methodName, logToRoot)

    @staticmethod
    def __getMethod():
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        classFile = ResMan.getFileName(calframe[3].filename)
        function = calframe[3].function
        return f"{Logger.BOLD}{classFile}->{function}: {Logger.ENDC}"

    @staticmethod
    def __infoPrint(message, header):
        return header + message

    @staticmethod
    def __okBluePrint(message, header):
        return header + Logger.OKBLUE + message + Logger.ENDC

    @staticmethod
    def __okCyanPrint(message, header):
        return header + Logger.OKCYAN + message + Logger.ENDC

    @staticmethod
    def __okGreenPrint(message, header):
        return header + Logger.OKGREEN + message + Logger.ENDC

    @staticmethod
    def __warningPrint(message, header):
        return header + Logger.WARNING + message + Logger.ENDC

    @staticmethod
    def __failPrint(message, header):
        return header + Logger.FAIL + message + Logger.ENDC

    @staticmethod
    def __boldPrint(message, header):
        return header + Logger.BOLD + message + Logger.ENDC

    @staticmethod
    def __underlinePrint(message, header):
        return header + Logger.UNDERLINE + message + Logger.ENDC
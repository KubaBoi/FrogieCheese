import inspect
from os import stat
import threading
from datetime import datetime

from cheese.resourceManager import ResMan

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
    def info(message):
        header = Logger.__getMethod()
        Logger.writeInFile(header + message)
        x = threading.Thread(target=Logger.__infoPrint, args=(message,header,))
        x.start()

    @staticmethod
    def okBlue(message):
        header = Logger.__getMethod()
        Logger.writeInFile(header + message)
        x = threading.Thread(target=Logger.__okBluePrint, args=(message,header,))
        x.start()

    @staticmethod
    def okCyan(message):
        header = Logger.__getMethod()
        Logger.writeInFile(header + message)
        x = threading.Thread(target=Logger.__okCyanPrint, args=(message,header,))
        x.start()

    @staticmethod
    def okGreen(message):
        header = Logger.__getMethod()
        Logger.writeInFile(header + message)
        x = threading.Thread(target=Logger.__okGreenPrint, args=(message,header,))
        x.start()

    @staticmethod
    def warning(message):
        header = Logger.__getMethod()
        Logger.writeInFile(header + message)
        x = threading.Thread(target=Logger.__warningPrint, args=(message,header,))
        x.start()

    @staticmethod
    def fail(message):
        header = Logger.__getMethod()
        Logger.writeInFile(header + message)
        x = threading.Thread(target=Logger.__failPrint, args=(message,header,))
        x.start()

    @staticmethod
    def bold(message):
        header = Logger.__getMethod()
        Logger.writeInFile(header + message)
        x = threading.Thread(target=Logger.__boldPrint, args=(message,header,))
        x.start()

    @staticmethod
    def underline(message):
        header = Logger.__getMethod()
        Logger.writeInFile(header + message)
        x = threading.Thread(target=Logger.__underlinePrint, args=(message,header,))
        x.start()

    #PRIVATE METHODS

    @staticmethod
    def writeInFile(log):
        with open(ResMan.cheese() + "/log.txt", "a") as f:
            f.write(log + "\n")

    @staticmethod
    def __getMethod():
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        classFile = ResMan.getFileName(calframe[3].filename)
        function = calframe[3].function
        date = datetime.now()
        return date.strftime("%H:%M:%S") + f" - {classFile}->{function}: "

    @staticmethod
    def __infoPrint(message, header):
        print(Logger.BOLD + header + Logger.ENDC + message)

    @staticmethod
    def __okBluePrint(message, header):
        print(Logger.BOLD + header + Logger.ENDC  + Logger.OKBLUE + message + Logger.ENDC)

    @staticmethod
    def __okCyanPrint(message, header):
        print(Logger.BOLD + header + Logger.ENDC  + Logger.OKCYAN + message + Logger.ENDC)

    @staticmethod
    def __okGreenPrint(message, header):
        print(Logger.BOLD + header + Logger.ENDC  + Logger.OKGREEN + message + Logger.ENDC)

    @staticmethod
    def __warningPrint(message, header):
        print(Logger.BOLD + header + Logger.ENDC  + Logger.WARNING + message + Logger.ENDC)

    @staticmethod
    def __failPrint(message, header):
        print(Logger.BOLD + header + Logger.ENDC  + Logger.FAIL + message + Logger.ENDC)

    @staticmethod
    def __boldPrint(message, header):
        print(Logger.BOLD + header + Logger.ENDC  + Logger.BOLD + message + Logger.ENDC)

    @staticmethod
    def __underlinePrint(message, header):
        print(Logger.BOLD + header + Logger.ENDC  + Logger.UNDERLINE + message + Logger.ENDC)
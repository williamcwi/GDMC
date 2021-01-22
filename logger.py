from datetime import datetime as dt
import os.path
import platform
import datetime

class Logger:

    def __init__(self, name):
        self.name = name

    def debug(self, message):
        log = '{} - {} - {} - {}'.format(dt.now(), self.name, 'DEBUG', message)
        print(log)
        self.to_file(log)

    def info(self, message):
        log = '{} - {} - {} - {}'.format(dt.now(), self.name, 'INFO', message)
        print(log)
        self.to_file(log)

    def warning(self, message):
        log = '{} - {} - {} - {}'.format(dt.now(), self.name, 'WARNING', message)
        print(log)
        self.to_file(log)

    def error(self, message):
        log = '{} - {} - {} - {}'.format(dt.now(), self.name, 'ERROR', message)
        print(log)
        self.to_file(log)

    def critical(self, message):
        log = '{} - {} - {} - {}'.format(dt.now(), self.name, 'CRITICAL', message)
        print(log)
        self.to_file(log)

    def to_file(self, log):
        if platform.system()==("Darwin") and int(platform.release()[:2]) >= 19:
            with open(os.path.join(os.path.expanduser("~/Desktop"), "gdmcLog" +'.txt'), 'a+') as f:
                f.write(log + '\n')
                f.close()
        else:
            with open(os.path.join(os.path.dirname(__file__),'logs', 'gdmc.log'), 'a+') as f:
                f.write(log + '\n')
                f.close()
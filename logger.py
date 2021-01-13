from datetime import datetime as dt
import os.path

class Logger:

    def __init__(self, name):
        self.name = name

    def debug(self, message):
        log = '{} - {} - {} - {}'.format(dt.now(), self.name, 'DEBUG', message)
        print(log)

    def info(self, message):
        log = '{} - {} - {} - {}'.format(dt.now(), self.name, 'INFO', message)
        print(log)

    def warning(self, message):
        log = '{} - {} - {} - {}'.format(dt.now(), self.name, 'WARNING', message)
        print(log)

    def error(self, message):
        log = '{} - {} - {} - {}'.format(dt.now(), self.name, 'ERROR', message)
        print(log)
        self.to_file(log)

    def critical(self, message):
        log = '{} - {} - {} - {}'.format(dt.now(), self.name, 'CRITICAL', message)
        print(log)

    def to_file(self, log):
        with open(os.path.join(os.path.dirname(__file__),'logs', 'gdmc.log'), 'a+') as f:
            f.write(log + '\n')
            f.close()
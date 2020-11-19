from datetime import datetime as dt

class Logger:

    def __init__(self, name):
        self.name = name

    def debug(self, message):
        print('{} - {} - {} - {}'.format(dt.now(), self.name, 'DEBUG', message))

    def info(self, message):
        print('{} - {} - {} - {}'.format(dt.now(), self.name, 'INFO', message))

    def warning(self, message):
        print('{} - {} - {} - {}'.format(dt.now(), self.name, 'WARNING', message))

    def error(self, message):
        print('{} - {} - {} - {}'.format(dt.now(), self.name, 'ERROR', message))

    def critical(self, message):
        print('{} - {} - {} - {}'.format(dt.now(), self.name, 'CRITICAL', message))
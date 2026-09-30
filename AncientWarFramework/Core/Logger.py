# -*- coding: utf-8 -*-

class Logger(object):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40

    LEVEL_NAMES = {DEBUG: "DEBUG", INFO: "INFO", WARNING: "WARN", ERROR: "ERROR"}

    def __init__(self, name="AWF", level=INFO):
        self.name = name
        self.level = level

    def _write(self, level, message):
        if level < self.level:
            return
        print("[%s][%s] %s" % (self.name, self.LEVEL_NAMES.get(level, str(level)), message))

    def debug(self, message):
        self._write(self.DEBUG, message)

    def info(self, message):
        self._write(self.INFO, message)

    def warning(self, message):
        self._write(self.WARNING, message)

    def error(self, message):
        self._write(self.ERROR, message)

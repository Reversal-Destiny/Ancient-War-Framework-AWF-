# -*- coding: utf-8 -*-

class Lifecycle(object):
    BOOTSTRAP = "bootstrap"
    REGISTER = "register"
    RESOLVE = "resolve"
    FREEZE = "freeze"
    RUNNING = "running"
    SHUTDOWN = "shutdown"

    ORDER = (BOOTSTRAP, REGISTER, RESOLVE, FREEZE, RUNNING, SHUTDOWN)

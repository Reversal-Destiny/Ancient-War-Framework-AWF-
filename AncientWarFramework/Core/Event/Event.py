# -*- coding: utf-8 -*-

class FrameworkEvent(object):
    """
    统一事件对象。cancel 与 stop_propagation 含义分离。
    """

    def __init__(self, name, data=None, source=None, target=None, context=None, result=None):
        self.name = str(name)
        self.data = data if data is not None else {}
        self.source = source
        self.target = target
        self.context = context
        self.result = result
        self._cancelled = False
        self._stopped = False

    def cancel(self, engine_cancel_key=None):
        self._cancelled = True
        if engine_cancel_key and isinstance(self.data, dict):
            self.data[engine_cancel_key] = True
        return self

    def is_cancelled(self):
        return self._cancelled

    def stop_propagation(self):
        self._stopped = True
        return self

    def is_propagation_stopped(self):
        return self._stopped

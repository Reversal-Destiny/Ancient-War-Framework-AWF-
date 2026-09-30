# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Event.Event import FrameworkEvent


def _function_metadata(bound_method, attr_name):
    func = getattr(bound_method, "im_func", None) or getattr(bound_method, "__func__", None) or bound_method
    return getattr(func, attr_name, ())


class EventBus(object):
    def __init__(self, logger=None, profiler=None, raise_errors=False):
        self.logger = logger
        self.profiler = profiler
        self.raise_errors = raise_errors
        self._listeners = {}

    def register(self, name, callback, priority=0, owner=None):
        name = str(name)
        bucket = self._listeners.setdefault(name, [])
        bucket.append((int(priority), callback, owner))
        bucket.sort(key=lambda value: value[0], reverse=True)
        return callback

    def unregister_owner(self, owner):
        for name in list(self._listeners.keys()):
            self._listeners[name] = [item for item in self._listeners[name] if item[2] is not owner]
            if not self._listeners[name]:
                del self._listeners[name]

    def register_owner(self, owner):
        for attr_name in dir(owner):
            callback = getattr(owner, attr_name, None)
            if not callable(callback):
                continue
            for meta in _function_metadata(callback, "__awf_events__"):
                self.register(meta["name"], callback, meta["priority"], owner)

    def emit(self, event_or_name, data=None, source=None, target=None, context=None):
        if isinstance(event_or_name, FrameworkEvent):
            evt = event_or_name
        else:
            evt = FrameworkEvent(event_or_name, data, source, target, context)
        listeners = list(self._listeners.get(evt.name, ()))
        for priority, callback, owner in listeners:
            if evt.is_propagation_stopped():
                break
            token = self.profiler.begin("event", evt.name, callback) if self.profiler else None
            try:
                value = callback(evt)
                if value is not None:
                    evt.result = value
            except Exception as error:
                if self.logger:
                    self.logger.error("event %s listener %r failed: %s" % (evt.name, callback, error))
                if self.raise_errors:
                    raise
            finally:
                if self.profiler:
                    self.profiler.end(token)
        return evt

    def listeners(self, name=None):
        if name is None:
            return dict((key, list(value)) for key, value in self._listeners.items())
        return list(self._listeners.get(str(name), ()))

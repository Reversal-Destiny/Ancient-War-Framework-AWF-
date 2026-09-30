# -*- coding: utf-8 -*-

# Portions of the public decorator design are derived from QuModLibs' @Listen
# pattern. AWF stores metadata only; registration is explicit during Feature load.


def _append_metadata(func, attr_name, value):
    values = list(getattr(func, attr_name, ()))
    values.append(value)
    setattr(func, attr_name, tuple(values))
    return func


def event(name, priority=0):
    def decorator(func):
        return _append_metadata(func, "__awf_events__", {"name": str(name), "priority": int(priority)})
    return decorator


def engine_event(event_name, priority=0, namespace=None, system_name=None):
    def decorator(func):
        return _append_metadata(func, "__awf_engine_events__", {
            "event_name": str(event_name),
            "priority": int(priority),
            "namespace": namespace,
            "system_name": system_name,
        })
    return decorator

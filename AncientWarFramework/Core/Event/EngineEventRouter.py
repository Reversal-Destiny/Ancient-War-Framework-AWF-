# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Event.Event import FrameworkEvent
from AncientWarFramework.Core.Event.EventBus import _function_metadata


class EngineEventRouter(object):
    """
    将网易原生事件转换为 AWF EventBus 事件。
    """

    def __init__(self, runtime):
        self.runtime = runtime
        self._native_keys = set()
        self._wrappers = []

    def _bus_name(self, namespace, system_name, event_name):
        return "engine:%s:%s:%s" % (namespace, system_name, event_name)

    def register_owner(self, owner):
        for attr_name in dir(owner):
            callback = getattr(owner, attr_name, None)
            if not callable(callback):
                continue
            for meta in _function_metadata(callback, "__awf_engine_events__"):
                namespace = meta.get("namespace") or self.runtime.adapter.engine_namespace()
                system_name = meta.get("system_name") or self.runtime.adapter.engine_system_name()
                event_name = meta["event_name"]
                bus_name = self._bus_name(namespace, system_name, event_name)
                self.runtime.event_bus.register(bus_name, callback, meta.get("priority", 0), owner)
                self._ensure_native(namespace, system_name, event_name, bus_name)

    def _ensure_native(self, namespace, system_name, event_name, bus_name):
        key = (namespace, system_name, event_name)
        if key in self._native_keys:
            return
        self._native_keys.add(key)

        def wrapper(args):
            evt = FrameworkEvent(
                bus_name,
                data=args,
                source=args.get("srcId") if isinstance(args, dict) else None,
                target=args.get("entityId") if isinstance(args, dict) else None,
                context=self.runtime,
            )
            self.runtime.event_bus.emit(evt)

        self._wrappers.append(wrapper)
        self.runtime.system.ListenForEvent(namespace, system_name, event_name, self.runtime.system, wrapper)

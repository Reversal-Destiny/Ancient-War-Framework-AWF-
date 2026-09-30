# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Exceptions import RegistryConflictError, RegistryFrozenError
from AncientWarFramework.Core.Lifecycle import Lifecycle


class Registry(object):
    """
    分阶段 Registry；默认 FREEZE 后只读。
    """

    allow_runtime_register = False

    def __init__(self, registry_id, runtime=None):
        self.registry_id = str(registry_id)
        self.runtime = runtime
        self.phase = Lifecycle.BOOTSTRAP
        self._values = {}
        self._sources = {}

    def set_phase(self, phase):
        self.phase = phase

    def _ensure_mutable(self):
        if self.phase in (Lifecycle.FREEZE, Lifecycle.RUNNING) and not self.allow_runtime_register:
            raise RegistryFrozenError("registry %s is frozen" % self.registry_id)

    def register(self, key, value, source=None, replace=False):
        self._ensure_mutable()
        key = str(key)
        if key in self._values and not replace:
            raise RegistryConflictError("registry %s duplicate key: %s" % (self.registry_id, key))
        if self.runtime and self.phase == Lifecycle.RUNNING:
            before = self.runtime.event_bus.emit("registry.before_change", data={"registry": self, "action": "register", "key": key, "value": value})
            if before.is_cancelled():
                return None
        self._values[key] = value
        self._sources[key] = source
        if self.runtime and self.phase == Lifecycle.RUNNING:
            self.runtime.event_bus.emit("registry.changed", data={"registry": self, "action": "register", "key": key, "value": value})
        return value

    def unregister(self, key):
        self._ensure_mutable()
        key = str(key)
        if key not in self._values:
            return None
        if self.runtime and self.phase == Lifecycle.RUNNING:
            before = self.runtime.event_bus.emit("registry.before_change", data={"registry": self, "action": "unregister", "key": key})
            if before.is_cancelled():
                return None
        value = self._values.pop(key)
        self._sources.pop(key, None)
        if self.runtime and self.phase == Lifecycle.RUNNING:
            self.runtime.event_bus.emit("registry.changed", data={"registry": self, "action": "unregister", "key": key, "value": value})
        return value

    def get(self, key, default=None):
        return self._values.get(str(key), default)

    def require(self, key):
        key = str(key)
        if key not in self._values:
            raise KeyError("registry %s missing key: %s" % (self.registry_id, key))
        return self._values[key]

    def has(self, key):
        return str(key) in self._values

    def keys(self):
        return list(self._values.keys())

    def values(self):
        return list(self._values.values())

    def items(self):
        return list(self._values.items())

    def get_source(self, key):
        return self._sources.get(str(key))

    def __len__(self):
        return len(self._values)

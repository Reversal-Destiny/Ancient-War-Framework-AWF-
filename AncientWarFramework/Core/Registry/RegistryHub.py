# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Exceptions import RegistryConflictError


class RegistryHub(object):
    def __init__(self):
        self._registries = {}
        self._phase = None

    def register(self, registry, replace=False):
        key = registry.registry_id
        if key in self._registries and not replace:
            raise RegistryConflictError("registry already exists: %s" % key)
        self._registries[key] = registry
        if self._phase is not None:
            registry.set_phase(self._phase)
        return registry

    def get(self, registry_id, default=None):
        return self._registries.get(str(registry_id), default)

    def require(self, registry_id):
        registry = self.get(registry_id)
        if registry is None:
            raise KeyError("registry not found: %s" % registry_id)
        return registry

    def set_phase(self, phase):
        self._phase = phase
        for registry in self._registries.values():
            registry.set_phase(phase)

    def items(self):
        return list(self._registries.items())

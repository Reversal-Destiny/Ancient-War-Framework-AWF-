# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Feature.Feature import Feature
from AncientWarFramework.Core.Registry.Registry import Registry
from AncientWarFramework.Core.Result import Result


class SoldierRegistry(Registry):
    def __init__(self, runtime):
        Registry.__init__(self, "soldier_type", runtime)
        self._entity_index = {}

    def register_soldier(self, soldier_id, entity_id, faction_id=None, tags=(), controllable=True, data=None, source=None):
        value = dict(data or {})
        value.update({"id": str(soldier_id), "entity_id": str(entity_id), "faction_id": faction_id, "tags": tuple(tags), "controllable": bool(controllable)})
        self.register(soldier_id, value, source)
        self._entity_index[str(entity_id)] = str(soldier_id)
        return value

    def by_entity_identifier(self, entity_identifier):
        soldier_id = self._entity_index.get(str(entity_identifier))
        return self.get(soldier_id) if soldier_id else None


class SoldierService(object):
    def __init__(self, runtime, registry):
        self.runtime = runtime
        self.registry = registry

    def get_type(self, entity_id):
        try:
            identifier = self.runtime.adapter.get_identifier(entity_id)
        except Exception:
            return None
        return self.registry.by_entity_identifier(identifier)

    def is_soldier(self, entity_id):
        return self.get_type(entity_id) is not None

    def set_group(self, entity_id, group_id):
        self.runtime.adapter.set_mod_attr(entity_id, self.runtime.config.data_key("soldier_group"), int(group_id), True)
        return Result.success({"entity_id": entity_id, "group_id": int(group_id)})

    def get_group(self, entity_id, default=0):
        try:
            return int(self.runtime.adapter.get_mod_attr(entity_id, self.runtime.config.data_key("soldier_group"), default))
        except Exception:
            return int(default)


class SoldierFeature(Feature):
    feature_id = "soldier"
    dependencies = ("faction",)
    sides = ("server",)

    def register(self):
        registry = self.runtime.registries.register(SoldierRegistry(self.runtime))
        self.runtime.services.register("soldier", SoldierService(self.runtime, registry))

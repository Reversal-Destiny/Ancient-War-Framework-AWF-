# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Feature.Feature import Feature
from AncientWarFramework.Core.Registry.Registry import Registry
from AncientWarFramework.Core.Result import Result


class SpawnRegistry(Registry):
    def __init__(self, runtime):
        Registry.__init__(self, "spawn", runtime)

    def register_spawn(self, spawn_id, entity_id, events=(), data=None, source=None):
        value = dict(data or {})
        value.update({"id": str(spawn_id), "entity_id": str(entity_id), "events": tuple(events)})
        return self.register(spawn_id, value, source)


class SpawnService(object):
    def __init__(self, runtime, registry):
        self.runtime = runtime
        self.registry = registry

    def spawn(self, spawn_id, pos, dimension_id=0, rot=(0, 0)):
        definition = self.registry.get(spawn_id)
        if not definition:
            return Result.fail("unknown_spawn")
        entity_id = self.runtime.adapter.create_entity(definition["entity_id"], pos, rot, dimension_id)
        if not entity_id or entity_id == "-1":
            return Result.fail("spawn_failed")
        for event_name in definition.get("events", ()):
            self.runtime.adapter.trigger_entity_event(entity_id, event_name)
        self.runtime.event_bus.emit("spawn.entity_created", data={"spawn_id": spawn_id, "entity_id": entity_id})
        return Result.success({"entity_id": entity_id})


class SpawnFeature(Feature):
    feature_id = "spawn"
    sides = ("server",)

    def register(self):
        registry = self.runtime.registries.register(SpawnRegistry(self.runtime))
        self.runtime.services.register("spawn", SpawnService(self.runtime, registry))

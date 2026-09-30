# -*- coding: utf-8 -*-

import random

from AncientWarFramework.Core.Feature.Feature import Feature
from AncientWarFramework.Core.Registry.Registry import Registry
from AncientWarFramework.Core.Result import Result


class PatrolRegistry(Registry):
    def __init__(self, runtime):
        Registry.__init__(self, "patrol", runtime)

    def register_patrol(self, patrol_id, members, weight=1, formation_id="grid", spacing=1.5, data=None, source=None):
        value = dict(data or {})
        value.update({"id": str(patrol_id), "members": dict(members), "weight": max(0, int(weight)), "formation_id": formation_id, "spacing": float(spacing)})
        return self.register(patrol_id, value, source)


class PatrolService(object):
    def __init__(self, runtime, registry):
        self.runtime = runtime
        self.registry = registry

    def choose(self, patrol_ids=None):
        values = []
        total = 0
        for patrol_id in (patrol_ids or self.registry.keys()):
            patrol = self.registry.get(patrol_id)
            if not patrol:
                continue
            weight = max(0, int(patrol.get("weight", 0)))
            if weight <= 0:
                continue
            total += weight
            values.append((total, patrol))
        if total <= 0:
            return None
        value = random.randint(1, total)
        for upper, patrol in values:
            if value <= upper:
                return patrol
        return values[-1][1]

    def spawn_patrol(self, patrol_id, center, dimension_id=0, forward=(0.0, 1.0)):
        patrol = self.registry.get(patrol_id)
        if not patrol:
            return Result.fail("unknown_patrol")
        spawn_service = self.runtime.services.require("spawn")
        members = []
        spawn_ids = []
        for spawn_id, count in patrol.get("members", {}).items():
            for index in range(int(count)):
                spawn_ids.append(spawn_id)
        formation = self.runtime.services.require("formation").build_slots(
            center, len(spawn_ids), patrol.get("formation_id", "grid"), dimension_id,
            patrol.get("spacing", 1.5), forward, True)
        if not formation.ok:
            return formation
        for spawn_id, pos in zip(spawn_ids, formation.data):
            result = spawn_service.spawn(spawn_id, pos, dimension_id)
            if result.ok:
                members.append(result.data["entity_id"])
        self.runtime.event_bus.emit("patrol.spawned", data={"patrol_id": patrol_id, "entity_ids": members})
        return Result.success({"entity_ids": members})


class PatrolFeature(Feature):
    feature_id = "patrol"
    dependencies = ("spawn", "formation", "soldier")
    sides = ("server",)

    def register(self):
        registry = self.runtime.registries.register(PatrolRegistry(self.runtime))
        self.runtime.services.register("patrol", PatrolService(self.runtime, registry))

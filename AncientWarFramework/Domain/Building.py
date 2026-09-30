# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Feature.Feature import Feature
from AncientWarFramework.Core.Registry.Registry import Registry
from AncientWarFramework.Core.Result import Result


class BuildingRegistry(Registry):
    def __init__(self, runtime):
        Registry.__init__(self, "building", runtime)

    def register_building(self, building_id, costs=None, validator=None, placement_handler=None, data=None, source=None):
        value = dict(data or {})
        value.update({"id": str(building_id), "costs": dict(costs or {}), "validator": validator, "placement_handler": placement_handler})
        return self.register(building_id, value, source)


class BuildingService(object):
    def __init__(self, runtime, registry):
        self.runtime = runtime
        self.registry = registry

    def build(self, player_id, building_id, context):
        definition = self.registry.get(building_id)
        if not definition:
            return Result.fail("unknown_building")
        validator = definition.get("validator")
        if validator:
            validation = validator(player_id, context, definition)
            if isinstance(validation, Result) and not validation.ok:
                return validation
            if validation is False:
                return Result.fail("invalid_position")
        placement = definition.get("placement_handler")
        if placement is None:
            return Result.fail("placement_handler_missing")
        resources = self.runtime.services.require("resource")
        snapshot = resources.snapshot(player_id)
        consumed = resources.consume(player_id, definition.get("costs", {}))
        if not consumed.ok:
            return consumed
        try:
            result = placement(player_id, context, definition)
            if not isinstance(result, Result):
                result = Result.success(result) if result is not False else Result.fail("placement_failed")
            if not result.ok:
                resources.restore(player_id, snapshot)
                return result
        except Exception:
            resources.restore(player_id, snapshot)
            raise
        self.runtime.event_bus.emit("building.placed", data={"player_id": player_id, "building_id": building_id, "context": context})
        return result


class BuildingFeature(Feature):
    feature_id = "building"
    dependencies = ("resource", "faction")
    sides = ("server",)

    def register(self):
        registry = self.runtime.registries.register(BuildingRegistry(self.runtime))
        self.runtime.services.register("building", BuildingService(self.runtime, registry))

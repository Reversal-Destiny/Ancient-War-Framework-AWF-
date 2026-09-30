# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Data import Model, DictField, Repository, ModAttrBackend
from AncientWarFramework.Core.Feature.Feature import Feature
from AncientWarFramework.Core.Registry.Registry import Registry
from AncientWarFramework.Core.Result import Result


class PlayerResourceData(Model):
    values = DictField(default=dict, nullable=False)
    version = 1


class ResourceRegistry(Registry):
    def __init__(self, runtime):
        Registry.__init__(self, "resource", runtime)

    def register_resource(self, resource_id, display_name=None, minimum=0, data=None, source=None):
        value = dict(data or {})
        value.update({"id": str(resource_id), "display_name": display_name or str(resource_id), "minimum": int(minimum)})
        return self.register(resource_id, value, source)


class ResourceService(object):
    def __init__(self, runtime, registry, repository):
        self.runtime = runtime
        self.registry = registry
        self.repository = repository

    def get_all(self, player_id):
        return dict(self.repository.load(player_id).values)

    def get(self, player_id, resource_id):
        return int(self.repository.load(player_id).values.get(resource_id, 0))

    def set(self, player_id, resource_id, value):
        if not self.registry.has(resource_id):
            return Result.fail("unknown_resource", {"resource_id": resource_id})
        definition = self.registry.require(resource_id)
        value = int(value)
        if value < int(definition.get("minimum", 0)):
            return Result.fail("resource_below_minimum")
        model = self.repository.load(player_id)
        model.values = dict(model.values)
        model.values[resource_id] = value
        self.repository.save(player_id, model)
        self.runtime.event_bus.emit("resource.changed", data={"player_id": player_id, "resource_id": resource_id, "value": value})
        return Result.success({"resource_id": resource_id, "value": value})

    def add(self, player_id, resource_id, amount):
        return self.set(player_id, resource_id, self.get(player_id, resource_id) + int(amount))

    def can_afford(self, player_id, costs):
        for resource_id, amount in dict(costs or {}).items():
            if not self.registry.has(resource_id):
                return False
            try:
                amount = int(amount)
            except Exception:
                return False
            if amount < 0 or self.get(player_id, resource_id) < amount:
                return False
        return True

    def consume(self, player_id, costs):
        costs = dict(costs or {})
        for resource_id, amount in costs.items():
            if not self.registry.has(resource_id):
                return Result.fail("unknown_resource", {"resource_id": resource_id})
            try:
                amount = int(amount)
            except Exception:
                return Result.fail("invalid_resource_cost", {"resource_id": resource_id})
            if amount < 0:
                return Result.fail("invalid_resource_cost", {"resource_id": resource_id})
            costs[resource_id] = amount
        if not self.can_afford(player_id, costs):
            return Result.fail("not_enough_resource")
        model = self.repository.load(player_id)
        values = dict(model.values)
        for resource_id, amount in costs.items():
            values[resource_id] = int(values.get(resource_id, 0)) - int(amount)
        model.values = values
        self.repository.save(player_id, model)
        return Result.success({"costs": costs})

    def snapshot(self, player_id):
        return self.get_all(player_id)

    def restore(self, player_id, snapshot):
        model = self.repository.load(player_id)
        model.values = dict(snapshot)
        return self.repository.save(player_id, model)


class ResourceFeature(Feature):
    feature_id = "resource"
    sides = ("server",)

    def register(self):
        registry = self.runtime.registries.register(ResourceRegistry(self.runtime))
        PlayerResourceData.storage_key = self.runtime.config.data_key("player_resources")
        repo = Repository(PlayerResourceData, ModAttrBackend(self.runtime.adapter), PlayerResourceData.storage_key)
        self.runtime.services.register("resource", ResourceService(self.runtime, registry, repo))

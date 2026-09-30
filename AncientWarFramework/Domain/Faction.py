# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Data import Model, StringField, Repository, ModAttrBackend
from AncientWarFramework.Core.Feature.Feature import Feature
from AncientWarFramework.Core.Registry.Registry import Registry
from AncientWarFramework.Core.Result import Result


class PlayerFactionData(Model):
    faction_id = StringField(default=None, nullable=True)
    version = 1


class FactionRegistry(Registry):
    def __init__(self, runtime):
        Registry.__init__(self, "faction", runtime)

    def register_faction(self, faction_id, display_name=None, families=(), data=None, source=None):
        value = dict(data or {})
        value.update({"id": str(faction_id), "display_name": display_name or str(faction_id), "families": tuple(families)})
        return self.register(faction_id, value, source)


class FactionService(object):
    def __init__(self, runtime, registry, repository):
        self.runtime = runtime
        self.registry = registry
        self.repository = repository

    def get_player_faction(self, player_id):
        return self.repository.load(player_id).faction_id

    def set_player_faction(self, player_id, faction_id):
        if faction_id is not None and not self.registry.has(faction_id):
            return Result.fail("unknown_faction", {"faction_id": faction_id})
        model = self.repository.load(player_id)
        model.faction_id = faction_id
        self.repository.save(player_id, model)
        self.runtime.event_bus.emit("faction.player_changed", data={"player_id": player_id, "faction_id": faction_id})
        return Result.success({"faction_id": faction_id})

    def get_entity_faction(self, entity_id):
        try:
            value = self.runtime.adapter.get_mod_attr(
                entity_id, self.runtime.config.data_key("entity_faction"), None)
            if value and self.registry.has(value):
                return value
        except Exception:
            pass
        soldier_service = self.runtime.services.get("soldier")
        if soldier_service is not None:
            soldier_type = soldier_service.get_type(entity_id)
            if soldier_type and soldier_type.get("faction_id"):
                return soldier_type.get("faction_id")
        try:
            families = set(self.runtime.adapter.get_type_family(entity_id) or [])
        except Exception:
            families = set()
        for faction_id, info in self.registry.items():
            if families.intersection(info.get("families", ())):
                return faction_id
        return None

    def set_entity_faction(self, entity_id, faction_id):
        if faction_id is not None and not self.registry.has(faction_id):
            return Result.fail("unknown_faction")
        self.runtime.adapter.set_mod_attr(entity_id, self.runtime.config.data_key("entity_faction"), faction_id, True)
        return Result.success({"faction_id": faction_id})


class FactionFeature(Feature):
    feature_id = "faction"
    sides = ("server",)

    def register(self):
        registry = self.runtime.registries.register(FactionRegistry(self.runtime))
        PlayerFactionData.storage_key = self.runtime.config.data_key("player_faction")
        repo = Repository(PlayerFactionData, ModAttrBackend(self.runtime.adapter), PlayerFactionData.storage_key)
        self.runtime.services.register("faction", FactionService(self.runtime, registry, repo))

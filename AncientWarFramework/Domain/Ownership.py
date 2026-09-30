# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Feature.Feature import Feature


class OwnershipService(object):
    def __init__(self, runtime):
        self.runtime = runtime

    def get_owner_id(self, entity_id):
        try:
            return self.runtime.adapter.get_owner_id(entity_id)
        except Exception:
            return None

    def is_owned_by(self, entity_id, player_id):
        return self.get_owner_id(entity_id) == player_id

    def is_controllable_by(self, entity_id, player_id):
        soldier = self.runtime.services.require("soldier").get_type(entity_id)
        if not soldier or not soldier.get("controllable", True):
            return False
        if not self.is_owned_by(entity_id, player_id):
            return False
        faction = self.runtime.services.require("faction")
        player_faction = faction.get_player_faction(player_id)
        entity_faction = faction.get_entity_faction(entity_id)
        if player_faction and entity_faction and player_faction != entity_faction:
            return False
        return True


class OwnershipFeature(Feature):
    feature_id = "ownership"
    dependencies = ("soldier",)
    sides = ("server",)

    def register(self):
        self.runtime.services.register("ownership", OwnershipService(self.runtime))

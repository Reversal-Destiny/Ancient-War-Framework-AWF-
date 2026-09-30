# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Feature.Feature import Feature
from AncientWarFramework.Core.Registry.Registry import Registry


class Relation(object):
    FRIENDLY = "friendly"
    NEUTRAL = "neutral"
    HOSTILE = "hostile"


class CombatRelationRegistry(Registry):
    allow_runtime_register = True

    def __init__(self, runtime):
        Registry.__init__(self, "combat_relation", runtime)

    @staticmethod
    def key(first, second):
        return "%s|%s" % (first, second)

    def set_relation(self, first, second, relation, symmetric=True):
        self.register(self.key(first, second), relation, replace=True)
        if symmetric:
            self.register(self.key(second, first), relation, replace=True)


class CombatRelationService(object):
    def __init__(self, runtime, registry):
        self.runtime = runtime
        self.registry = registry

    def relation(self, first_faction, second_faction):
        if not first_faction or not second_faction:
            return Relation.NEUTRAL
        explicit = self.registry.get(self.registry.key(first_faction, second_faction))
        if explicit:
            return explicit
        return Relation.FRIENDLY if first_faction == second_faction else Relation.HOSTILE

    def entity_relation(self, first_entity, second_entity):
        faction = self.runtime.services.require("faction")
        return self.relation(faction.get_entity_faction(first_entity), faction.get_entity_faction(second_entity))

    def can_damage(self, first_entity, second_entity, friendly_fire=False):
        relation = self.entity_relation(first_entity, second_entity)
        return not (relation == Relation.FRIENDLY and not friendly_fire)


class CombatRelationFeature(Feature):
    feature_id = "combat_relation"
    dependencies = ("faction",)
    sides = ("server",)

    def register(self):
        registry = self.runtime.registries.register(CombatRelationRegistry(self.runtime))
        self.runtime.services.register("combat_relation", CombatRelationService(self.runtime, registry))

# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Data import Model, ListField, DictField, IntField, Repository, ModAttrBackend
from AncientWarFramework.Core.Feature.Feature import Feature
from AncientWarFramework.Core.Registry.Registry import Registry
from AncientWarFramework.Core.Result import Result


class PlayerTechnologyData(Model):
    researched = ListField(default=list, nullable=False)
    branches = DictField(default=dict, nullable=False)
    age = IntField(default=1, nullable=False)
    version = 1


class TechnologyRegistry(Registry):
    def __init__(self, runtime):
        Registry.__init__(self, "technology", runtime)

    def register_technology(self, tech_id, costs=None, prerequisites=(), faction_id=None, required_age=1, branch_group=None, target_age=None, data=None, source=None):
        value = dict(data or {})
        value.update({
            "id": str(tech_id), "costs": dict(costs or {}), "prerequisites": tuple(prerequisites),
            "faction_id": faction_id, "required_age": int(required_age), "branch_group": branch_group, "target_age": target_age,
        })
        return self.register(tech_id, value, source)


class TechnologyService(object):
    def __init__(self, runtime, registry, repository):
        self.runtime = runtime
        self.registry = registry
        self.repository = repository

    def get_state(self, player_id):
        return self.repository.load(player_id)

    def has(self, player_id, tech_id):
        return tech_id in self.get_state(player_id).researched

    def research(self, player_id, tech_id):
        tech = self.registry.get(tech_id)
        if not tech:
            return Result.fail("unknown_technology")
        model = self.repository.load(player_id)
        if tech_id in model.researched:
            return Result.fail("already_researched")
        faction_id = tech.get("faction_id")
        if faction_id and self.runtime.services.require("faction").get_player_faction(player_id) != faction_id:
            return Result.fail("wrong_faction")
        if model.age < int(tech.get("required_age", 1)):
            return Result.fail("age_locked")
        for prerequisite in tech.get("prerequisites", ()):
            if prerequisite not in model.researched:
                return Result.fail("missing_prerequisite", {"tech_id": prerequisite})
        branch = tech.get("branch_group")
        if branch and model.branches.get(branch) not in (None, tech_id):
            return Result.fail("branch_locked", {"selected": model.branches.get(branch)})
        resources = self.runtime.services.require("resource")
        snapshot = resources.snapshot(player_id)
        consumed = resources.consume(player_id, tech.get("costs", {}))
        if not consumed.ok:
            return consumed
        old = (list(model.researched), dict(model.branches), model.age)
        try:
            model.researched = list(model.researched) + [tech_id]
            branches = dict(model.branches)
            if branch:
                branches[branch] = tech_id
            model.branches = branches
            if tech.get("target_age") is not None:
                model.age = int(tech.get("target_age"))
            self.repository.save(player_id, model)
        except Exception:
            model.researched, model.branches, model.age = old
            resources.restore(player_id, snapshot)
            raise
        self.runtime.event_bus.emit("technology.researched", data={"player_id": player_id, "tech_id": tech_id})
        return Result.success({"tech_id": tech_id, "age": model.age})


class TechnologyFeature(Feature):
    feature_id = "technology"
    dependencies = ("resource", "faction")
    sides = ("server",)

    def register(self):
        registry = self.runtime.registries.register(TechnologyRegistry(self.runtime))
        PlayerTechnologyData.storage_key = self.runtime.config.data_key("player_technology")
        repo = Repository(PlayerTechnologyData, ModAttrBackend(self.runtime.adapter), PlayerTechnologyData.storage_key)
        self.runtime.services.register("technology", TechnologyService(self.runtime, registry, repo))

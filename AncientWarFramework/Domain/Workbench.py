# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Feature.Feature import Feature
from AncientWarFramework.Core.Registry.Registry import Registry
from AncientWarFramework.Core.Result import Result


class WorkbenchRegistry(Registry):
    def __init__(self, runtime):
        Registry.__init__(self, "workbench", runtime)

    def register_workbench(self, workbench_id, recipes=None, data=None, source=None):
        value = dict(data or {})
        value.update({"id": str(workbench_id), "recipes": dict(recipes or {})})
        return self.register(workbench_id, value, source)


class WorkbenchService(object):
    def __init__(self, runtime, registry):
        self.runtime = runtime
        self.registry = registry

    def get_payload(self, player_id, workbench_id):
        workbench = self.registry.get(workbench_id)
        if not workbench:
            return Result.fail("unknown_workbench")
        return Result.success({"workbench": workbench_id, "recipes": workbench.get("recipes", {}), "resources": self.runtime.services.require("resource").get_all(player_id)})

    def craft(self, player_id, workbench_id, recipe_id, count=1):
        workbench = self.registry.get(workbench_id)
        if not workbench:
            return Result.fail("unknown_workbench")
        recipe = workbench.get("recipes", {}).get(recipe_id)
        if not recipe:
            return Result.fail("unknown_recipe")
        try:
            count = int(count)
        except Exception:
            return Result.fail("invalid_count")
        if count <= 0 or count > int(recipe.get("max_count", 64)):
            return Result.fail("invalid_count")
        costs = dict((key, int(value) * count) for key, value in dict(recipe.get("costs", {})).items())
        resources = self.runtime.services.require("resource")
        snapshot = resources.snapshot(player_id)
        consumed = resources.consume(player_id, costs)
        if not consumed.ok:
            return consumed
        handler = recipe.get("output_handler")
        if handler:
            try:
                output = handler(player_id, recipe, count)
            except Exception:
                resources.restore(player_id, snapshot)
                raise
            if output is False:
                resources.restore(player_id, snapshot)
                return Result.fail("output_failed")
            if isinstance(output, Result) and not output.ok:
                resources.restore(player_id, snapshot)
                return output
        self.runtime.event_bus.emit("workbench.crafted", data={"player_id": player_id, "workbench_id": workbench_id, "recipe_id": recipe_id, "count": count})
        return Result.success({"recipe_id": recipe_id, "count": count})


class WorkbenchFeature(Feature):
    feature_id = "workbench"
    dependencies = ("resource",)
    sides = ("server",)

    def register(self):
        registry = self.runtime.registries.register(WorkbenchRegistry(self.runtime))
        self.runtime.services.register("workbench", WorkbenchService(self.runtime, registry))

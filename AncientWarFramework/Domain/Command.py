# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Feature.Feature import Feature
from AncientWarFramework.Core.Registry.Registry import Registry
from AncientWarFramework.Core.Result import Result
from AncientWarFramework.Core.RPC.Decorators import rpc_server


class CommandRegistry(Registry):
    allow_runtime_register = True

    def __init__(self, runtime):
        Registry.__init__(self, "command", runtime)

    def register_command(self, command_id, handler, requires_target=False, radius=24, data=None, source=None):
        value = dict(data or {})
        value.update({"id": str(command_id), "handler": handler, "requires_target": bool(requires_target), "radius": max(1, int(radius))})
        return self.register(command_id, value, source)


class CommandService(object):
    def __init__(self, runtime, registry):
        self.runtime = runtime
        self.registry = registry

    def _group_candidates(self, player_id, group_id, radius):
        soldier = self.runtime.services.require("soldier")
        ownership = self.runtime.services.require("ownership")
        result = []
        for entity_id in self.runtime.adapter.get_nearby_entities(player_id, int(radius)):
            if not ownership.is_controllable_by(entity_id, player_id):
                continue
            if group_id != "all" and soldier.get_group(entity_id) != int(group_id):
                continue
            result.append(entity_id)
        return result

    def resolve_selection(self, player_id, selection, group_id=0, radius=24):
        selection = selection if isinstance(selection, dict) else {}
        mode = selection.get("mode", "group")
        if mode == "single":
            entity_id = selection.get("entity_id")
            if not self.runtime.services.require("ownership").is_controllable_by(entity_id, player_id):
                return Result.fail("not_controllable", {"entity_id": entity_id})
            return Result.success([entity_id])
        if mode != "group":
            return Result.fail("invalid_selection_mode", {"mode": mode})
        if group_id != "all":
            try:
                group_id = int(group_id)
            except Exception:
                return Result.fail("invalid_group_id", {"group_id": group_id})
        return Result.success(self._group_candidates(player_id, group_id, radius))

    def execute(self, ctx, command_id, selection=None, target=None, group_id=0, params=None):
        command = self.registry.get(command_id)
        if not command:
            return Result.fail("unknown_command", {"command_id": command_id})
        selected = self.resolve_selection(ctx.player_id, selection, group_id, command.get("radius", 24))
        if not selected.ok:
            return selected
        entities = selected.data
        if not entities:
            return Result.fail("no_responsive_soldiers")
        if command.get("requires_target") and not target:
            return Result.fail("target_required")
        before = self.runtime.event_bus.emit("soldier.command.before_execute", data={
            "ctx": ctx, "command_id": command_id, "entities": entities, "target": target, "params": params or {},
        })
        if before.is_cancelled():
            return Result.fail("command_cancelled", before.result)
        result = command["handler"](ctx, entities, target, params or {})
        if not isinstance(result, Result):
            result = Result.success(result)
        self.runtime.event_bus.emit("soldier.command.after_execute", data={
            "ctx": ctx, "command_id": command_id, "entities": entities, "target": target, "result": result,
        })
        return result


class CommandFeature(Feature):
    feature_id = "command"
    dependencies = ("soldier", "ownership", "formation", "combat_relation")
    sides = ("server",)

    def register(self):
        registry = self.runtime.registries.register(CommandRegistry(self.runtime))
        self.runtime.services.register("command", CommandService(self.runtime, registry))

    @rpc_server("soldier.command")
    def rpc_command(self, ctx, data):
        data = data if isinstance(data, dict) else {}
        return self.runtime.services.require("command").execute(
            ctx,
            data.get("command_id"),
            data.get("selection"),
            data.get("target"),
            data.get("group_id", 0),
            data.get("params", {}),
        )

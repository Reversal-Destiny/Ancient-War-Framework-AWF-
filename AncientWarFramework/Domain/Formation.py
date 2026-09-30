# -*- coding: utf-8 -*-

import math

from AncientWarFramework.Core.Feature.Feature import Feature
from AncientWarFramework.Core.Registry.Registry import Registry
from AncientWarFramework.Core.Result import Result


class FormationProvider(object):
    def offsets(self, count, spacing=1.5):
        raise NotImplementedError


class LineFormation(FormationProvider):
    def offsets(self, count, spacing=1.5):
        start = -0.5 * (count - 1) * spacing
        return [(start + index * spacing, 0.0) for index in range(count)]


class ColumnFormation(FormationProvider):
    def offsets(self, count, spacing=1.5):
        return [(0.0, index * spacing) for index in range(count)]


class GridFormation(FormationProvider):
    def offsets(self, count, spacing=1.5):
        width = max(1, int(math.ceil(math.sqrt(count))))
        result = []
        for index in range(count):
            row, col = divmod(index, width)
            result.append(((col - (width - 1) * 0.5) * spacing, row * spacing))
        return result


class WedgeFormation(FormationProvider):
    def offsets(self, count, spacing=1.5):
        result = [(0.0, 0.0)]
        layer = 1
        while len(result) < count:
            result.append((-layer * spacing, layer * spacing))
            if len(result) < count:
                result.append((layer * spacing, layer * spacing))
            layer += 1
        return result[:count]


class FormationRegistry(Registry):
    def __init__(self, runtime):
        Registry.__init__(self, "formation", runtime)


class FormationService(object):
    def __init__(self, runtime, registry):
        self.runtime = runtime
        self.registry = registry

    def build_slots(self, center, count, formation_id="grid", dimension_id=0, spacing=1.5, forward=(0.0, 1.0), adapt_surface=True):
        provider = self.registry.get(formation_id)
        if provider is None:
            return Result.fail("unknown_formation", {"formation_id": formation_id})
        if count <= 0:
            return Result.success([])
        fx, fz = forward[0], forward[1]
        length = math.sqrt(fx * fx + fz * fz)
        if length <= 0.0001:
            fx, fz, length = 0.0, 1.0, 1.0
        fx, fz = fx / length, fz / length
        rx, rz = fz, -fx
        cx, cy, cz = center
        slots = []
        for lateral, depth in provider.offsets(int(count), float(spacing)):
            x = cx + rx * lateral + fx * depth
            z = cz + rz * lateral + fz * depth
            y = cy
            if adapt_surface:
                try:
                    surface_y = self.runtime.adapter.get_surface_y(x, z, dimension_id)
                    y = cy if surface_y is None else surface_y
                except Exception:
                    y = cy
            slots.append((x, y, z))
        return Result.success(slots)


class FormationFeature(Feature):
    feature_id = "formation"
    sides = ("server",)

    def register(self):
        registry = self.runtime.registries.register(FormationRegistry(self.runtime))
        registry.register("line", LineFormation(), source="awf")
        registry.register("column", ColumnFormation(), source="awf")
        registry.register("grid", GridFormation(), source="awf")
        registry.register("wedge", WedgeFormation(), source="awf")
        self.runtime.services.register("formation", FormationService(self.runtime, registry))

# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Exceptions import FeatureDependencyError, FeatureError
from AncientWarFramework.Core.Lifecycle import Lifecycle


class FeatureManager(object):
    def __init__(self, runtime):
        self.runtime = runtime
        self.feature_classes = []
        self.features = {}
        self.order = []

    def load(self, feature_classes):
        self.feature_classes = [cls for cls in feature_classes if self.runtime.side in getattr(cls, "sides", ("server", "client"))]
        self._validate_and_sort()
        for feature_id in self.order:
            cls = self.features[feature_id]
            self.features[feature_id] = cls(self.runtime)

    def _validate_and_sort(self):
        classes = {}
        for cls in self.feature_classes:
            feature_id = getattr(cls, "feature_id", None)
            if not feature_id:
                raise FeatureError("feature_id missing on %r" % cls)
            if feature_id in classes:
                raise FeatureError("duplicate feature_id: %s" % feature_id)
            classes[feature_id] = cls
        self.features = dict(classes)
        visiting = set()
        visited = set()
        order = []

        def visit(feature_id):
            if feature_id in visited:
                return
            if feature_id in visiting:
                raise FeatureDependencyError("feature dependency cycle at %s" % feature_id)
            cls = classes.get(feature_id)
            if cls is None:
                raise FeatureDependencyError("feature dependency missing: %s" % feature_id)
            visiting.add(feature_id)
            for dep in getattr(cls, "dependencies", ()):
                if dep not in classes:
                    raise FeatureDependencyError("feature %s requires missing %s" % (feature_id, dep))
                visit(dep)
            visiting.remove(feature_id)
            visited.add(feature_id)
            order.append(feature_id)

        for cls in self.feature_classes:
            visit(getattr(cls, "feature_id"))
        self.order = order

    def register_all(self):
        self.runtime.lifecycle = Lifecycle.REGISTER
        self.runtime.registries.set_phase(Lifecycle.REGISTER)
        for feature_id in self.order:
            feature = self.features[feature_id]
            feature.register()
            self.runtime.event_bus.register_owner(feature)
            self.runtime.engine_events.register_owner(feature)
            self.runtime.rpc.register_owner(feature)

    def resolve_all(self):
        self.runtime.lifecycle = Lifecycle.RESOLVE
        self.runtime.registries.set_phase(Lifecycle.RESOLVE)
        for feature_id in self.order:
            self.features[feature_id].resolve()

    def enable_all(self):
        self.runtime.lifecycle = Lifecycle.FREEZE
        self.runtime.registries.set_phase(Lifecycle.FREEZE)
        self.runtime.lifecycle = Lifecycle.RUNNING
        self.runtime.registries.set_phase(Lifecycle.RUNNING)
        for feature_id in self.order:
            self.features[feature_id].enable()

    def shutdown(self):
        self.runtime.lifecycle = Lifecycle.SHUTDOWN
        for feature_id in reversed(self.order):
            feature = self.features.get(feature_id)
            if feature:
                try:
                    feature.disable()
                finally:
                    self.runtime.event_bus.unregister_owner(feature)
                    self.runtime.rpc.unregister_owner(feature)

    def get(self, feature_id):
        value = self.features.get(str(feature_id))
        return value if not isinstance(value, type) else None

    def describe(self):
        result = []
        for feature_id in self.order:
            feature = self.features.get(feature_id)
            result.append({"id": feature_id, "dependencies": list(getattr(feature, "dependencies", ())), "side": self.runtime.side})
        return result

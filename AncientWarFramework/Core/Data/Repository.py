# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Data.Migration import MigrationPlan
from AncientWarFramework.Core.Exceptions import DataError


class Repository(object):
    """
    以一个 envelope 保存 Model：{version, data}。
    """

    def __init__(self, model_class, backend, storage_key=None, cache=True, migrations=None):
        self.model_class = model_class
        self.backend = backend
        self.storage_key = storage_key or model_class.storage_key
        if not self.storage_key:
            raise DataError("model storage_key is required")
        self.cache_enabled = cache
        self.cache = {}
        self.migrations = migrations or MigrationPlan()

    def load(self, subject_id, refresh=False):
        cache_key = str(subject_id)
        if self.cache_enabled and not refresh and cache_key in self.cache:
            return self.cache[cache_key]
        raw = self.backend.load(subject_id, self.storage_key)
        if not isinstance(raw, dict):
            model = self.model_class()
        else:
            version = int(raw.get("version", 1))
            data = raw.get("data", {})
            target_version = int(self.model_class.version)
            if version < target_version:
                data = self.migrations.migrate(data, version, target_version)
            elif version > target_version:
                raise DataError("stored model version %s is newer than supported %s" % (version, target_version))
            model = self.model_class.from_dict(data)
        if self.cache_enabled:
            self.cache[cache_key] = model
        return model

    def save(self, subject_id, model):
        value = {"version": int(self.model_class.version), "data": model.to_dict()}
        ok = self.backend.save(subject_id, self.storage_key, value)
        if ok and self.cache_enabled:
            self.cache[str(subject_id)] = model
        return ok

    def delete(self, subject_id):
        self.cache.pop(str(subject_id), None)
        return self.backend.delete(subject_id, self.storage_key)

    def invalidate(self, subject_id=None):
        if subject_id is None:
            self.cache.clear()
        else:
            self.cache.pop(str(subject_id), None)

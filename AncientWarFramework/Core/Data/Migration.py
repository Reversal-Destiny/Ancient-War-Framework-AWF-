# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Exceptions import DataMigrationError


class MigrationPlan(object):
    def __init__(self):
        self._steps = {}

    def add(self, from_version, callback):
        self._steps[int(from_version)] = callback
        return self

    def migrate(self, data, from_version, to_version):
        current = int(from_version)
        value = data
        while current < int(to_version):
            callback = self._steps.get(current)
            if callback is None:
                raise DataMigrationError("missing migration %s -> %s" % (current, current + 1))
            value = callback(value)
            current += 1
        return value

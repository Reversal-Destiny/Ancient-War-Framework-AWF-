# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Data.Field import Field


class Model(object):
    storage_key = None
    version = 1

    def __init__(self, **kwargs):
        self._values = {}
        for name, field in self.fields().items():
            setattr(self, name, kwargs.get(name, field.default_value()))

    @classmethod
    def fields(cls):
        result = {}
        for base in reversed(cls.__mro__):
            for name, value in getattr(base, "__dict__", {}).items():
                if isinstance(value, Field):
                    value.name = name
                    result[name] = value
        return result

    def to_dict(self):
        return dict((name, getattr(self, name)) for name in self.fields())

    @classmethod
    def from_dict(cls, data):
        data = data if isinstance(data, dict) else {}
        return cls(**data)

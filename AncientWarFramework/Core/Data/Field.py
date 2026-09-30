# -*- coding: utf-8 -*-

class Field(object):
    expected_type = None

    def __init__(self, default=None, nullable=True, validator=None):
        self.default = default
        self.nullable = nullable
        self.validator = validator
        self.name = None

    def default_value(self):
        if callable(self.default):
            return self.default()
        if isinstance(self.default, dict):
            return dict(self.default)
        if isinstance(self.default, list):
            return list(self.default)
        return self.default

    def validate(self, value):
        if value is None:
            if not self.nullable:
                raise ValueError("field %s cannot be None" % self.name)
            return value
        if self.expected_type is not None and not isinstance(value, self.expected_type):
            raise TypeError("field %s expected %r, got %r" % (self.name, self.expected_type, type(value)))
        if self.validator and not self.validator(value):
            raise ValueError("field %s validator rejected value" % self.name)
        return value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance._values.get(self.name, self.default_value())

    def __set__(self, instance, value):
        instance._values[self.name] = self.validate(value)


class StringField(Field):
    try:
        expected_type = (str, unicode)
    except NameError:
        expected_type = (str,)


class IntField(Field):
    try:
        expected_type = (int, long)
    except NameError:
        expected_type = (int,)


class FloatField(Field):
    expected_type = (int, float)


class BoolField(Field):
    expected_type = (bool,)


class ListField(Field):
    expected_type = (list, tuple)


class DictField(Field):
    expected_type = (dict,)

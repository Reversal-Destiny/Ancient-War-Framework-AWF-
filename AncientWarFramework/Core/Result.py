# -*- coding: utf-8 -*-

class Result(object):
    """
    业务结果；用于正常成功/拒绝，不代表程序异常。
    """

    def __init__(self, ok, code="success", data=None, message=None):
        # type: (bool, str, object, str) -> None
        self.ok = bool(ok)
        self.code = str(code)
        self.data = data
        self.message = message

    @classmethod
    def success(cls, data=None, code="success", message=None):
        # type: (object, str, str) -> Result
        return cls(True, code, data, message)

    @classmethod
    def fail(cls, code, data=None, message=None):
        # type: (str, object, str) -> Result
        return cls(False, code, data, message)

    def to_dict(self):
        # type: () -> dict
        return {"ok": self.ok, "code": self.code, "data": self.data, "message": self.message}

    @classmethod
    def from_dict(cls, value):
        # type: (dict) -> Result
        if not isinstance(value, dict):
            return cls.fail("invalid_result", value)
        return cls(value.get("ok", False), value.get("code", "unknown"), value.get("data"), value.get("message"))

    def __nonzero__(self):
        return self.ok

    def __bool__(self):
        return self.ok

    def __repr__(self):
        return "Result(ok=%r, code=%r, data=%r)" % (self.ok, self.code, self.data)

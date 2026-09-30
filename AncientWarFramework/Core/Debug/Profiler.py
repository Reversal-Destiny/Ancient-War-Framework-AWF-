# -*- coding: utf-8 -*-

import time


class Profiler(object):
    def __init__(self, enabled=False, slow_ms=5.0, logger=None):
        self.enabled = enabled
        self.slow_ms = float(slow_ms)
        self.logger = logger
        self.stats = {}

    def begin(self, category, name, callback=None):
        if not self.enabled:
            return None
        return (category, name, callback, time.time())

    def end(self, token):
        if not self.enabled or token is None:
            return
        category, name, callback, started = token
        elapsed = (time.time() - started) * 1000.0
        key = (category, name, repr(callback))
        stat = self.stats.setdefault(key, {"count": 0, "total_ms": 0.0, "max_ms": 0.0})
        stat["count"] += 1
        stat["total_ms"] += elapsed
        stat["max_ms"] = max(stat["max_ms"], elapsed)
        if self.logger and elapsed >= self.slow_ms:
            self.logger.warning("slow %s %s: %.3fms callback=%r" % (category, name, elapsed, callback))

    def snapshot(self):
        result = []
        for key, stat in self.stats.items():
            item = dict(stat)
            item["category"], item["name"], item["callback"] = key
            item["avg_ms"] = item["total_ms"] / max(1, item["count"])
            result.append(item)
        return result

# -*- coding: utf-8 -*-

class TimerManager(object):
    def __init__(self, runtime):
        self.runtime = runtime
        self.records = []

    def once(self, delay, callback, *args):
        timer = self.runtime.adapter.add_timer(delay, callback, *args)
        self.records.append(("once", timer, callback))
        return timer

    def repeat(self, interval, callback, *args):
        timer = self.runtime.adapter.add_repeated_timer(interval, callback, *args)
        self.records.append(("repeat", timer, callback))
        return timer

    def inspect(self):
        return list(self.records)

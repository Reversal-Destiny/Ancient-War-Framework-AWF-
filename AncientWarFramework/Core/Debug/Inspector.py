# -*- coding: utf-8 -*-

class Inspector(object):
    def __init__(self, runtime):
        self.runtime = runtime

    def features(self):
        return self.runtime.feature_manager.describe()

    def events(self, name=None):
        return self.runtime.event_bus.listeners(name)

    def rpc(self):
        return {"server": sorted(self.runtime.rpc.server_endpoints.keys()), "client": sorted(self.runtime.rpc.client_endpoints.keys())}

    def registries(self):
        return dict((key, registry.keys()) for key, registry in self.runtime.registries.items())

    def services(self):
        return [key for key, value in self.runtime.services.items()]

    def timers(self):
        return self.runtime.timers.inspect()

    def profiler(self):
        return self.runtime.profiler.snapshot()

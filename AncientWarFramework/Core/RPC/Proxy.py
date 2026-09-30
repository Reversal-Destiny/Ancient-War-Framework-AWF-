# -*- coding: utf-8 -*-

class RPCNamespaceProxy(object):
    def __init__(self, manager, target, path="", player_id=None):
        self.manager = manager
        self.target = target
        self.path = path
        self.player_id = player_id

    def __getattr__(self, item):
        path = item if not self.path else self.path + "." + item
        return RPCNamespaceProxy(self.manager, self.target, path, self.player_id)

    def __call__(self, data=None, callback=None):
        data = {} if data is None else data
        if self.target == "server":
            if callback is not None:
                return self.manager.request_server(self.path, data, callback)
            return self.manager.notify_server(self.path, data)
        return self.manager.notify_client(self.player_id, self.path, data)

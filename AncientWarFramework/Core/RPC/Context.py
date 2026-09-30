# -*- coding: utf-8 -*-

class RPCContext(object):
    def __init__(self, side, endpoint, player_id=None, request_id=None, raw=None, runtime=None):
        self.side = side
        self.endpoint = endpoint
        self.player_id = player_id
        self.request_id = request_id
        self.raw = raw
        self.runtime = runtime

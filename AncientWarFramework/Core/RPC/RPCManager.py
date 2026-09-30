# -*- coding: utf-8 -*-

import time

from AncientWarFramework.Core.Exceptions import RPCError
from AncientWarFramework.Core.Result import Result
from AncientWarFramework.Core.RPC.Context import RPCContext
from AncientWarFramework.Core.RPC.Proxy import RPCNamespaceProxy


def _function_metadata(bound_method, attr_name):
    func = getattr(bound_method, "im_func", None) or getattr(bound_method, "__func__", None) or bound_method
    return getattr(func, attr_name, ())


class RPCManager(object):
    """
    基于单个 C2S/S2C 自定义事件的 endpoint RPC。
    """

    def __init__(self, runtime):
        self.runtime = runtime
        self.server_endpoints = {}
        self.client_endpoints = {}
        self.pending = {}
        self._request_seq = 0
        self.server = RPCNamespaceProxy(self, "server")

    def client(self, player_id):
        return RPCNamespaceProxy(self, "client", player_id=player_id)

    def bind(self):
        cfg = self.runtime.config
        sys = self.runtime.system
        if self.runtime.side == "server":
            sys.DefineEvent(cfg.rpc_s2c_event)
            sys.ListenForEvent(cfg.mod_name, cfg.client_name, cfg.rpc_c2s_event, sys, self._on_server_packet)
        else:
            sys.DefineEvent(cfg.rpc_c2s_event)
            sys.ListenForEvent(cfg.mod_name, cfg.server_name, cfg.rpc_s2c_event, sys, self._on_client_packet)

    def register_owner(self, owner):
        for attr_name in dir(owner):
            callback = getattr(owner, attr_name, None)
            if not callable(callback):
                continue
            for endpoint in _function_metadata(callback, "__awf_rpc_server__"):
                if endpoint in self.server_endpoints:
                    raise RPCError("duplicate server endpoint: %s" % endpoint)
                self.server_endpoints[endpoint] = (callback, owner)
            for endpoint in _function_metadata(callback, "__awf_rpc_client__"):
                if endpoint in self.client_endpoints:
                    raise RPCError("duplicate client endpoint: %s" % endpoint)
                self.client_endpoints[endpoint] = (callback, owner)

    def unregister_owner(self, owner):
        self.server_endpoints = dict((k, v) for k, v in self.server_endpoints.items() if v[1] is not owner)
        self.client_endpoints = dict((k, v) for k, v in self.client_endpoints.items() if v[1] is not owner)

    def _next_request_id(self):
        self._request_seq += 1
        return "%s-%s" % (int(time.time() * 1000), self._request_seq)

    def notify_server(self, endpoint, data):
        if self.runtime.side != "client":
            raise RPCError("notify_server is client-only")
        self.runtime.system.NotifyToServer(self.runtime.config.rpc_c2s_event, {
            "kind": "call", "endpoint": endpoint, "data": data,
        })
        return True

    def request_server(self, endpoint, data, callback):
        if self.runtime.side != "client":
            raise RPCError("request_server is client-only")
        request_id = self._next_request_id()
        self.pending[request_id] = callback
        self.runtime.system.NotifyToServer(self.runtime.config.rpc_c2s_event, {
            "kind": "call", "endpoint": endpoint, "data": data, "request_id": request_id,
        })
        return request_id

    def notify_client(self, player_id, endpoint, data):
        if self.runtime.side != "server":
            raise RPCError("notify_client is server-only")
        if not player_id:
            return False
        self.runtime.system.NotifyToClient(player_id, self.runtime.config.rpc_s2c_event, {
            "kind": "call", "endpoint": endpoint, "data": data,
        })
        return True

    def _serialize_result(self, value):
        if isinstance(value, Result):
            return {"__awf_result__": True, "value": value.to_dict()}
        return value

    def _deserialize_result(self, value):
        if isinstance(value, dict) and value.get("__awf_result__"):
            return Result.from_dict(value.get("value", {}))
        return value

    def _on_server_packet(self, args):
        if not isinstance(args, dict):
            return
        if args.get("kind") != "call":
            return
        # QuModLibs' loader uses the engine-injected __id__ as the RPC sender identity.
        # AWF follows the same security boundary and never trusts payload player_id.
        player_id = args.get("__id__")
        endpoint = args.get("endpoint")
        request_id = args.get("request_id")
        if not player_id:
            self.runtime.logger.warning("RPC rejected without engine sender identity: %s" % endpoint)
            return
        record = self.server_endpoints.get(endpoint)
        if not record:
            result = Result.fail("rpc_endpoint_not_found", {"endpoint": endpoint})
        else:
            callback = record[0]
            ctx = RPCContext("server", endpoint, player_id, request_id, args, self.runtime)
            try:
                result = callback(ctx, args.get("data"))
            except Exception as error:
                self.runtime.logger.error("RPC server endpoint %s failed: %s" % (endpoint, error))
                result = Result.fail("rpc_internal_error")
                if self.runtime.config.raise_rpc_errors:
                    raise
        if request_id:
            self.runtime.system.NotifyToClient(player_id, self.runtime.config.rpc_s2c_event, {
                "kind": "response", "request_id": request_id, "value": self._serialize_result(result),
            })

    def _on_client_packet(self, args):
        if not isinstance(args, dict):
            return
        kind = args.get("kind")
        if kind == "response":
            request_id = args.get("request_id")
            callback = self.pending.pop(request_id, None)
            if callback:
                callback(self._deserialize_result(args.get("value")))
            return
        if kind != "call":
            return
        endpoint = args.get("endpoint")
        record = self.client_endpoints.get(endpoint)
        if not record:
            self.runtime.logger.warning("RPC client endpoint not found: %s" % endpoint)
            return
        ctx = RPCContext("client", endpoint, self.runtime.adapter.local_player_id(), args.get("request_id"), args, self.runtime)
        record[0](ctx, args.get("data"))

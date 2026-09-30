# -*- coding: utf-8 -*-

# The decorator concept is derived from QuModLibs @AllowCall / InjectRPCPlayerId.
# Unlike QuModLibs, AWF decorators only store metadata and handlers receive RPCContext.


def _rpc_meta(func, attr_name, endpoint):
    values = list(getattr(func, attr_name, ()))
    values.append(str(endpoint))
    setattr(func, attr_name, tuple(values))
    return func


def rpc_server(endpoint):
    def decorator(func):
        return _rpc_meta(func, "__awf_rpc_server__", endpoint)
    return decorator


def rpc_client(endpoint):
    def decorator(func):
        return _rpc_meta(func, "__awf_rpc_client__", endpoint)
    return decorator

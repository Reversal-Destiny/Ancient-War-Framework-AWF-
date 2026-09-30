# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Exceptions import ConfigurationError
from AncientWarFramework.Core.Logger import Logger

_CONFIG = None


class FrameworkConfig(object):
    def __init__(self, mod_name, server_name, client_name, features=(), data_prefix=None,
                 dev_mode=False, profiler_enabled=False, profiler_slow_ms=5.0,
                 log_level=Logger.INFO, raise_event_errors=False, raise_rpc_errors=False,
                 rpc_c2s_event="__awf_rpc_c2s__", rpc_s2c_event="__awf_rpc_s2c__"):
        self.mod_name = str(mod_name)
        self.server_name = str(server_name)
        self.client_name = str(client_name)
        self.features = tuple(features)
        self.data_prefix = data_prefix or self.mod_name + ".awf"
        self.dev_mode = bool(dev_mode)
        self.profiler_enabled = bool(profiler_enabled)
        self.profiler_slow_ms = float(profiler_slow_ms)
        self.log_level = log_level
        self.raise_event_errors = bool(raise_event_errors)
        self.raise_rpc_errors = bool(raise_rpc_errors)
        self.rpc_c2s_event = str(rpc_c2s_event)
        self.rpc_s2c_event = str(rpc_s2c_event)

    def data_key(self, name):
        return "%s.%s" % (self.data_prefix, name)


def configure(config):
    global _CONFIG
    if not isinstance(config, FrameworkConfig):
        raise ConfigurationError("configure requires FrameworkConfig")
    _CONFIG = config
    return config


def get_config():
    if _CONFIG is None:
        raise ConfigurationError("AWF is not configured; call configure(FrameworkConfig(...)) before RegisterSystem")
    return _CONFIG

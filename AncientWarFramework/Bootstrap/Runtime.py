# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Adapter.ServerAdapter import ServerAdapter
from AncientWarFramework.Core.Adapter.ClientAdapter import ClientAdapter
from AncientWarFramework.Core.Debug.Inspector import Inspector
from AncientWarFramework.Core.Debug.Profiler import Profiler
from AncientWarFramework.Core.Event.EngineEventRouter import EngineEventRouter
from AncientWarFramework.Core.Event.EventBus import EventBus
from AncientWarFramework.Core.Feature.FeatureManager import FeatureManager
from AncientWarFramework.Core.Lifecycle import Lifecycle
from AncientWarFramework.Core.Logger import Logger
from AncientWarFramework.Core.Registry.RegistryHub import RegistryHub
from AncientWarFramework.Core.RPC.RPCManager import RPCManager
from AncientWarFramework.Core.Service.ServiceContainer import ServiceContainer
from AncientWarFramework.Core.Timer.TimerManager import TimerManager


class FrameworkRuntime(object):
    def __init__(self, side, system, config):
        self.side = side
        self.system = system
        self.config = config
        self.lifecycle = Lifecycle.BOOTSTRAP
        self.logger = Logger("AWF:%s" % side.upper(), config.log_level)
        self.profiler = Profiler(config.profiler_enabled, config.profiler_slow_ms, self.logger)
        self.services = ServiceContainer()
        self.registries = RegistryHub()
        self.event_bus = EventBus(self.logger, self.profiler, config.raise_event_errors)
        self.adapter = ServerAdapter(system) if side == "server" else ClientAdapter(system)
        self.rpc = RPCManager(self)
        self.timers = TimerManager(self)
        self.engine_events = EngineEventRouter(self)
        self.feature_manager = FeatureManager(self)
        self.inspector = Inspector(self)

    def start(self):
        self.logger.info("starting features=%s" % len(self.config.features))
        self.rpc.bind()
        self.feature_manager.load(self.config.features)
        self.feature_manager.register_all()
        self.feature_manager.resolve_all()
        self.feature_manager.enable_all()
        self.event_bus.emit("framework.started", data={"side": self.side}, context=self)

    def shutdown(self):
        self.event_bus.emit("framework.before_shutdown", data={"side": self.side}, context=self)
        self.feature_manager.shutdown()
        self.services.clear()
        self.logger.info("shutdown complete")

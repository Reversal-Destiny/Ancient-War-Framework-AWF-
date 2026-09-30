# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Exceptions import ServiceError


class ServiceContainer(object):
    """
    保存无玩家 scope 的框架级 Service。
    """

    def __init__(self):
        self._services = {}

    def register(self, service_id, service, replace=False):
        # type: (str, object, bool) -> object
        if service_id in self._services and not replace:
            raise ServiceError("service already registered: %s" % service_id)
        self._services[str(service_id)] = service
        return service

    def has(self, service_id):
        return str(service_id) in self._services

    def get(self, service_id, default=None):
        return self._services.get(str(service_id), default)

    def require(self, service_id):
        service = self.get(service_id)
        if service is None:
            raise ServiceError("required service not found: %s" % service_id)
        return service

    def unregister(self, service_id):
        return self._services.pop(str(service_id), None)

    def items(self):
        return list(self._services.items())

    def clear(self):
        self._services.clear()

# -*- coding: utf-8 -*-

try:
    import mod.client.extraClientApi as clientApi
except ImportError:
    clientApi = None


class ClientAdapter(object):
    def __init__(self, system):
        self.system = system
        self.api = clientApi
        self.comp_factory = clientApi.GetEngineCompFactory() if clientApi else None
        self.level_id = clientApi.GetLevelId() if clientApi else None

    def engine_namespace(self):
        return self.api.GetEngineNamespace()

    def engine_system_name(self):
        return self.api.GetEngineSystemName()

    def local_player_id(self):
        return self.api.GetLocalPlayerId()

    def get_pos(self, entity_id):
        return self.comp_factory.CreatePos(entity_id).GetPos()

    def get_foot_pos(self, entity_id):
        return self.comp_factory.CreatePos(entity_id).GetFootPos()

    def get_dimension(self, entity_id):
        return self.comp_factory.CreateDimension(entity_id).GetEntityDimensionId()

    def get_identifier(self, entity_id):
        return self.comp_factory.CreateEngineType(entity_id).GetEngineTypeStr()

    def get_mod_attr(self, entity_id, key, default=None):
        return self.comp_factory.CreateModAttr(entity_id).GetAttr(key, default)

    def add_timer(self, delay, callback, *args):
        return self.comp_factory.CreateGame(self.level_id).AddTimer(delay, callback, *args)

# -*- coding: utf-8 -*-

try:
    import mod.server.extraServerApi as serverApi
except ImportError:
    serverApi = None


class ServerAdapter(object):
    """
    网易服务端 ModAPI 薄封装；不建立第二套 Entity 对象模型。
    """

    def __init__(self, system):
        self.system = system
        self.api = serverApi
        self.comp_factory = serverApi.GetEngineCompFactory() if serverApi else None
        self.level_id = serverApi.GetLevelId() if serverApi else None

    def engine_namespace(self):
        return self.api.GetEngineNamespace()

    def engine_system_name(self):
        return self.api.GetEngineSystemName()

    def local_player_id(self):
        return None

    def get_pos(self, entity_id):
        return self.comp_factory.CreatePos(entity_id).GetPos()

    def get_foot_pos(self, entity_id):
        return self.comp_factory.CreatePos(entity_id).GetFootPos()

    def set_pos(self, entity_id, pos):
        return self.comp_factory.CreatePos(entity_id).SetPos(pos)

    def get_dimension(self, entity_id):
        return self.comp_factory.CreateDimension(entity_id).GetEntityDimensionId()

    def get_identifier(self, entity_id):
        return self.comp_factory.CreateEngineType(entity_id).GetEngineTypeStr()

    def get_type_family(self, entity_id):
        return self.comp_factory.CreateAttr(entity_id).GetTypeFamily() or []

    def get_owner_id(self, entity_id):
        return self.comp_factory.CreateTame(entity_id).GetOwnerId()

    def get_attack_target(self, entity_id):
        return self.comp_factory.CreateAction(entity_id).GetAttackTarget()

    def set_attack_target(self, entity_id, target_id):
        return self.comp_factory.CreateAction(entity_id).SetAttackTarget(target_id)

    def reset_attack_target(self, entity_id):
        return self.comp_factory.CreateAction(entity_id).ResetAttackTarget()

    def trigger_entity_event(self, entity_id, event_name):
        return self.comp_factory.CreateEntityEvent(entity_id).TriggerCustomEvent(entity_id, event_name)

    def get_mod_attr(self, entity_id, key, default=None):
        return self.comp_factory.CreateModAttr(entity_id).GetAttr(key, default)

    def set_mod_attr(self, entity_id, key, value, sync=True):
        return self.comp_factory.CreateModAttr(entity_id).SetAttr(key, value, sync)

    def get_extra_data(self, key, default=None):
        value = self.comp_factory.CreateExtraData(self.level_id).GetExtraData(key)
        return default if value is None else value

    def set_extra_data(self, key, value, sync=True):
        return self.comp_factory.CreateExtraData(self.level_id).SetExtraData(key, value, sync)

    def get_block_entity_data(self, subject_id):
        dimension_id, pos = subject_id
        return self.comp_factory.CreateBlockEntityData(self.level_id).GetBlockEntityData(dimension_id, tuple(pos))

    def get_surface_y(self, x, z, dimension_id):
        value = self.comp_factory.CreateBlockInfo(self.level_id).GetTopBlockHeight((int(x), int(z)), int(dimension_id))
        return None if value is None else value + 1

    def get_nearby_entities(self, center_entity_id, radius):
        radius = int(radius)
        result = set()
        game = self.comp_factory.CreateGame(self.level_id)
        try:
            mob_type = self.api.GetMinecraftEnum().EntityType.Mob
            for entity_id in game.GetEntitiesAroundByType(center_entity_id, radius, mob_type) or []:
                result.add(entity_id)
        except Exception:
            pass
        try:
            center = self.get_foot_pos(center_entity_id)
            dimension_id = self.get_dimension(center_entity_id)
            if center:
                x, y, z = center
                start = (int(x) - radius, int(y) - radius, int(z) - radius)
                end = (int(x) + radius, int(y) + radius, int(z) + radius)
                radius_sq = float(radius * radius)
                for entity_id in game.GetEntitiesInSquareArea(None, start, end, dimension_id) or []:
                    if entity_id == center_entity_id:
                        continue
                    pos = self.get_foot_pos(entity_id)
                    if not pos:
                        continue
                    dx, dy, dz = pos[0] - x, pos[1] - y, pos[2] - z
                    if dx * dx + dy * dy + dz * dz <= radius_sq:
                        result.add(entity_id)
        except Exception:
            pass
        return list(result)

    def create_entity(self, entity_identifier, pos, rot=(0, 0), dimension_id=0, is_npc=False):
        return self.system.CreateEngineEntityByTypeStr(entity_identifier, tuple(pos), tuple(rot), int(dimension_id), bool(is_npc))

    def destroy_entity(self, entity_id):
        if hasattr(self.system, "DestroyEntity"):
            return self.system.DestroyEntity(entity_id)
        return self.comp_factory.CreateGame(self.level_id).DestroyEntity(entity_id)

    def add_timer(self, delay, callback, *args):
        return self.comp_factory.CreateGame(self.level_id).AddTimer(delay, callback, *args)

    def add_repeated_timer(self, delay, callback, *args):
        return self.comp_factory.CreateGame(self.level_id).AddRepeatedTimer(delay, callback, *args)

# Complete Public Symbol Index

本索引由 v0.1.0 源码生成，列出 AWF 根包中所有非下划线公开类、模块函数和公开方法。语义、约束与示例见 `API_REFERENCE.md`、`EVENT_RPC_REFERENCE.md`、`DOMAIN_GUIDE.md`。

## `Bootstrap/ClientSystem.py`

- Class `AWFClientSystem`
  - `Update(self)`
  - `Destroy(self)`

## `Bootstrap/Config.py`

- Class `FrameworkConfig`
  - `data_key(self, name)`
- Function `configure(config)`
- Function `get_config()`

## `Bootstrap/Runtime.py`

- Class `FrameworkRuntime`
  - `start(self)`
  - `shutdown(self)`

## `Bootstrap/ServerSystem.py`

- Class `AWFServerSystem`
  - `Update(self)`
  - `Destroy(self)`

## `Core/Adapter/ClientAdapter.py`

- Class `ClientAdapter`
  - `engine_namespace(self)`
  - `engine_system_name(self)`
  - `local_player_id(self)`
  - `get_pos(self, entity_id)`
  - `get_foot_pos(self, entity_id)`
  - `get_dimension(self, entity_id)`
  - `get_identifier(self, entity_id)`
  - `get_mod_attr(self, entity_id, key, default=None)`
  - `add_timer(self, delay, callback, *args)`

## `Core/Adapter/ServerAdapter.py`

- Class `ServerAdapter`
  - `engine_namespace(self)`
  - `engine_system_name(self)`
  - `local_player_id(self)`
  - `get_pos(self, entity_id)`
  - `get_foot_pos(self, entity_id)`
  - `set_pos(self, entity_id, pos)`
  - `get_dimension(self, entity_id)`
  - `get_identifier(self, entity_id)`
  - `get_type_family(self, entity_id)`
  - `get_owner_id(self, entity_id)`
  - `get_attack_target(self, entity_id)`
  - `set_attack_target(self, entity_id, target_id)`
  - `reset_attack_target(self, entity_id)`
  - `trigger_entity_event(self, entity_id, event_name)`
  - `get_mod_attr(self, entity_id, key, default=None)`
  - `set_mod_attr(self, entity_id, key, value, sync=True)`
  - `get_extra_data(self, key, default=None)`
  - `set_extra_data(self, key, value, sync=True)`
  - `get_block_entity_data(self, subject_id)`
  - `get_surface_y(self, x, z, dimension_id)`
  - `get_nearby_entities(self, center_entity_id, radius)`
  - `create_entity(self, entity_identifier, pos, rot=(0, 0), dimension_id=0, is_npc=False)`
  - `destroy_entity(self, entity_id)`
  - `add_timer(self, delay, callback, *args)`
  - `add_repeated_timer(self, delay, callback, *args)`

## `Core/Data/Backend.py`

- Class `MemoryBackend`
  - `load(self, subject_id, storage_key)`
  - `save(self, subject_id, storage_key, value)`
  - `delete(self, subject_id, storage_key)`
- Class `ModAttrBackend`
  - `load(self, subject_id, storage_key)`
  - `save(self, subject_id, storage_key, value)`
  - `delete(self, subject_id, storage_key)`
- Class `ExtraDataBackend`
  - `load(self, subject_id, storage_key)`
  - `save(self, subject_id, storage_key, value)`
  - `delete(self, subject_id, storage_key)`
- Class `BlockEntityBackend`
  - `load(self, subject_id, storage_key)`
  - `save(self, subject_id, storage_key, value)`
  - `delete(self, subject_id, storage_key)`

## `Core/Data/Field.py`

- Class `Field`
  - `default_value(self)`
  - `validate(self, value)`
- Class `StringField`
- Class `IntField`
- Class `FloatField`
- Class `BoolField`
- Class `ListField`
- Class `DictField`

## `Core/Data/Migration.py`

- Class `MigrationPlan`
  - `add(self, from_version, callback)`
  - `migrate(self, data, from_version, to_version)`

## `Core/Data/Model.py`

- Class `Model`
  - `fields(cls)`
  - `to_dict(self)`
  - `from_dict(cls, data)`

## `Core/Data/Repository.py`

- Class `Repository`
  - `load(self, subject_id, refresh=False)`
  - `save(self, subject_id, model)`
  - `delete(self, subject_id)`
  - `invalidate(self, subject_id=None)`

## `Core/Debug/Inspector.py`

- Class `Inspector`
  - `features(self)`
  - `events(self, name=None)`
  - `rpc(self)`
  - `registries(self)`
  - `services(self)`
  - `timers(self)`
  - `profiler(self)`

## `Core/Debug/Profiler.py`

- Class `Profiler`
  - `begin(self, category, name, callback=None)`
  - `end(self, token)`
  - `snapshot(self)`

## `Core/Event/Decorators.py`

- Function `event(name, priority=0)`
- Function `engine_event(event_name, priority=0, namespace=None, system_name=None)`

## `Core/Event/EngineEventRouter.py`

- Class `EngineEventRouter`
  - `register_owner(self, owner)`

## `Core/Event/Event.py`

- Class `FrameworkEvent`
  - `cancel(self, engine_cancel_key=None)`
  - `is_cancelled(self)`
  - `stop_propagation(self)`
  - `is_propagation_stopped(self)`

## `Core/Event/EventBus.py`

- Class `EventBus`
  - `register(self, name, callback, priority=0, owner=None)`
  - `unregister_owner(self, owner)`
  - `register_owner(self, owner)`
  - `emit(self, event_or_name, data=None, source=None, target=None, context=None)`
  - `listeners(self, name=None)`

## `Core/Exceptions.py`

- Class `AWFError`
- Class `ConfigurationError`
- Class `FeatureError`
- Class `FeatureDependencyError`
- Class `RegistryError`
- Class `RegistryConflictError`
- Class `RegistryFrozenError`
- Class `ServiceError`
- Class `RPCError`
- Class `DataError`
- Class `DataMigrationError`

## `Core/Feature/Feature.py`

- Class `Feature`
  - `register(self)`
  - `resolve(self)`
  - `enable(self)`
  - `disable(self)`

## `Core/Feature/FeatureManager.py`

- Class `FeatureManager`
  - `load(self, feature_classes)`
  - `register_all(self)`
  - `resolve_all(self)`
  - `enable_all(self)`
  - `shutdown(self)`
  - `get(self, feature_id)`
  - `describe(self)`

## `Core/Lifecycle.py`

- Class `Lifecycle`

## `Core/Logger.py`

- Class `Logger`
  - `debug(self, message)`
  - `info(self, message)`
  - `warning(self, message)`
  - `error(self, message)`

## `Core/RPC/Context.py`

- Class `RPCContext`

## `Core/RPC/Decorators.py`

- Function `rpc_server(endpoint)`
- Function `rpc_client(endpoint)`

## `Core/RPC/Proxy.py`

- Class `RPCNamespaceProxy`

## `Core/RPC/RPCManager.py`

- Class `RPCManager`
  - `client(self, player_id)`
  - `bind(self)`
  - `register_owner(self, owner)`
  - `unregister_owner(self, owner)`
  - `notify_server(self, endpoint, data)`
  - `request_server(self, endpoint, data, callback)`
  - `notify_client(self, player_id, endpoint, data)`

## `Core/Registry/Registry.py`

- Class `Registry`
  - `set_phase(self, phase)`
  - `register(self, key, value, source=None, replace=False)`
  - `unregister(self, key)`
  - `get(self, key, default=None)`
  - `require(self, key)`
  - `has(self, key)`
  - `keys(self)`
  - `values(self)`
  - `items(self)`
  - `get_source(self, key)`

## `Core/Registry/RegistryHub.py`

- Class `RegistryHub`
  - `register(self, registry, replace=False)`
  - `get(self, registry_id, default=None)`
  - `require(self, registry_id)`
  - `set_phase(self, phase)`
  - `items(self)`

## `Core/Result.py`

- Class `Result`
  - `success(cls, data=None, code='success', message=None)`
  - `fail(cls, code, data=None, message=None)`
  - `to_dict(self)`
  - `from_dict(cls, value)`

## `Core/Service/ServiceContainer.py`

- Class `ServiceContainer`
  - `register(self, service_id, service, replace=False)`
  - `has(self, service_id)`
  - `get(self, service_id, default=None)`
  - `require(self, service_id)`
  - `unregister(self, service_id)`
  - `items(self)`
  - `clear(self)`

## `Core/Timer/TimerManager.py`

- Class `TimerManager`
  - `once(self, delay, callback, *args)`
  - `repeat(self, interval, callback, *args)`
  - `inspect(self)`

## `Core/UI/Controller.py`

- Class `UIController`
  - `find_path(self, root_path, suffix)`

## `Core/UI/Feature.py`

- Class `UIInfrastructureFeature`
  - `register(self)`
  - `on_ui_init_finished(self, event)`

## `Core/UI/PathResolver.py`

- Class `PathResolver`
  - `find_by_suffix(screen_node, root_path, suffix)`
  - `find_all_by_suffix(screen_node, root_path, suffix)`
  - `child_by_name(control, name)`

## `Core/UI/ScreenManager.py`

- Class `ScreenManager`
  - `register_all(self)`
  - `create(self, screen_id, options=None)`
  - `get(self, screen_id)`
  - `remove(self, screen_id)`

## `Core/UI/UIRegistry.py`

- Class `UIRegistry`
  - `register_screen(self, screen_id, ui_name, python_path, screen_def, is_hud=False, source=None)`

## `Domain/Building.py`

- Class `BuildingRegistry`
  - `register_building(self, building_id, costs=None, validator=None, placement_handler=None, data=None, source=None)`
- Class `BuildingService`
  - `build(self, player_id, building_id, context)`
- Class `BuildingFeature`
  - `register(self)`

## `Domain/CombatRelation.py`

- Class `Relation`
- Class `CombatRelationRegistry`
  - `key(first, second)`
  - `set_relation(self, first, second, relation, symmetric=True)`
- Class `CombatRelationService`
  - `relation(self, first_faction, second_faction)`
  - `entity_relation(self, first_entity, second_entity)`
  - `can_damage(self, first_entity, second_entity, friendly_fire=False)`
- Class `CombatRelationFeature`
  - `register(self)`

## `Domain/Command.py`

- Class `CommandRegistry`
  - `register_command(self, command_id, handler, requires_target=False, radius=24, data=None, source=None)`
- Class `CommandService`
  - `resolve_selection(self, player_id, selection, group_id=0, radius=24)`
  - `execute(self, ctx, command_id, selection=None, target=None, group_id=0, params=None)`
- Class `CommandFeature`
  - `register(self)`
  - `rpc_command(self, ctx, data)`

## `Domain/Faction.py`

- Class `PlayerFactionData`
- Class `FactionRegistry`
  - `register_faction(self, faction_id, display_name=None, families=(), data=None, source=None)`
- Class `FactionService`
  - `get_player_faction(self, player_id)`
  - `set_player_faction(self, player_id, faction_id)`
  - `get_entity_faction(self, entity_id)`
  - `set_entity_faction(self, entity_id, faction_id)`
- Class `FactionFeature`
  - `register(self)`

## `Domain/Formation.py`

- Class `FormationProvider`
  - `offsets(self, count, spacing=1.5)`
- Class `LineFormation`
  - `offsets(self, count, spacing=1.5)`
- Class `ColumnFormation`
  - `offsets(self, count, spacing=1.5)`
- Class `GridFormation`
  - `offsets(self, count, spacing=1.5)`
- Class `WedgeFormation`
  - `offsets(self, count, spacing=1.5)`
- Class `FormationRegistry`
- Class `FormationService`
  - `build_slots(self, center, count, formation_id='grid', dimension_id=0, spacing=1.5, forward=(0.0, 1.0), adapt_surface=True)`
- Class `FormationFeature`
  - `register(self)`

## `Domain/Ownership.py`

- Class `OwnershipService`
  - `get_owner_id(self, entity_id)`
  - `is_owned_by(self, entity_id, player_id)`
  - `is_controllable_by(self, entity_id, player_id)`
- Class `OwnershipFeature`
  - `register(self)`

## `Domain/Patrol.py`

- Class `PatrolRegistry`
  - `register_patrol(self, patrol_id, members, weight=1, formation_id='grid', spacing=1.5, data=None, source=None)`
- Class `PatrolService`
  - `choose(self, patrol_ids=None)`
  - `spawn_patrol(self, patrol_id, center, dimension_id=0, forward=(0.0, 1.0))`
- Class `PatrolFeature`
  - `register(self)`

## `Domain/Resource.py`

- Class `PlayerResourceData`
- Class `ResourceRegistry`
  - `register_resource(self, resource_id, display_name=None, minimum=0, data=None, source=None)`
- Class `ResourceService`
  - `get_all(self, player_id)`
  - `get(self, player_id, resource_id)`
  - `set(self, player_id, resource_id, value)`
  - `add(self, player_id, resource_id, amount)`
  - `can_afford(self, player_id, costs)`
  - `consume(self, player_id, costs)`
  - `snapshot(self, player_id)`
  - `restore(self, player_id, snapshot)`
- Class `ResourceFeature`
  - `register(self)`

## `Domain/Soldier.py`

- Class `SoldierRegistry`
  - `register_soldier(self, soldier_id, entity_id, faction_id=None, tags=(), controllable=True, data=None, source=None)`
  - `by_entity_identifier(self, entity_identifier)`
- Class `SoldierService`
  - `get_type(self, entity_id)`
  - `is_soldier(self, entity_id)`
  - `set_group(self, entity_id, group_id)`
  - `get_group(self, entity_id, default=0)`
- Class `SoldierFeature`
  - `register(self)`

## `Domain/Spawn.py`

- Class `SpawnRegistry`
  - `register_spawn(self, spawn_id, entity_id, events=(), data=None, source=None)`
- Class `SpawnService`
  - `spawn(self, spawn_id, pos, dimension_id=0, rot=(0, 0))`
- Class `SpawnFeature`
  - `register(self)`

## `Domain/Technology.py`

- Class `PlayerTechnologyData`
- Class `TechnologyRegistry`
  - `register_technology(self, tech_id, costs=None, prerequisites=(), faction_id=None, required_age=1, branch_group=None, target_age=None, data=None, source=None)`
- Class `TechnologyService`
  - `get_state(self, player_id)`
  - `has(self, player_id, tech_id)`
  - `research(self, player_id, tech_id)`
- Class `TechnologyFeature`
  - `register(self)`

## `Domain/Workbench.py`

- Class `WorkbenchRegistry`
  - `register_workbench(self, workbench_id, recipes=None, data=None, source=None)`
- Class `WorkbenchService`
  - `get_payload(self, player_id, workbench_id)`
  - `craft(self, player_id, workbench_id, recipe_id, count=1)`
- Class `WorkbenchFeature`
  - `register(self)`

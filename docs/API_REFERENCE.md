# AWF 0.1.0 API Reference

本文只描述 AWF 公开 API。以下接口均按 Python 2.7 风格设计。

## Bootstrap

### `FrameworkConfig(...)`

参数：`mod_name`、`server_name`、`client_name`、`features=()`、`data_prefix=None`、`dev_mode=False`、`profiler_enabled=False`、`profiler_slow_ms=5.0`、`log_level`、`raise_event_errors=False`、`raise_rpc_errors=False`、`rpc_c2s_event`、`rpc_s2c_event`。

`data_key(name)` 返回当前作品隔离的持久化 key。

### `configure(config)` / `get_config()`
必须在 `RegisterSystem` 前配置。未配置直接抛 `ConfigurationError`。

### `AWFServerSystem` / `AWFClientSystem`
唯一根 System。外部项目只负责注册它们，不应再为每个 Feature 创建网易 System。

## Result / Exceptions

### `Result.success(data=None, code="success", message=None)`
### `Result.fail(code, data=None, message=None)`
字段：`ok`、`code`、`data`、`message`。`to_dict()` / `from_dict()` 用于网络序列化。

程序结构错误使用 `AWFError` 子类：`ConfigurationError`、`FeatureDependencyError`、`RegistryConflictError`、`RegistryFrozenError`、`RPCError`、`DataError`、`DataMigrationError`。

## Feature

### `Feature`
类属性：`feature_id`、`dependencies`、`sides`。

生命周期方法：
- `register()`：注册 Registry / Service。
- `resolve()`：解析依赖。
- `enable()`：进入运行期。
- `disable()`：逆序关闭。

### `FeatureManager`
`load(feature_classes)`、`register_all()`、`resolve_all()`、`enable_all()`、`shutdown()`、`get(feature_id)`、`describe()`。

## Service

### `ServiceContainer`
- `register(service_id, service, replace=False)`
- `has(service_id)`
- `get(service_id, default=None)`
- `require(service_id)`
- `unregister(service_id)`
- `items()` / `clear()`

Service 应保存行为和框架级缓存，不保存“当前玩家”这类 per-player 状态。

## Registry

### `Registry(registry_id, runtime=None)`
- `register(key, value, source=None, replace=False)`
- `unregister(key)`
- `get/require/has`
- `keys/values/items`
- `get_source(key)`
- `set_phase(phase)`

默认在 FREEZE/RUNNING 禁止修改。子类可声明 `allow_runtime_register = True`。

### `RegistryHub`
`register(registry)`、`get/require`、`set_phase()`、`items()`。

## Event

### `@event(name, priority=0)`
声明 Domain Event listener。装饰器只保存 metadata。

### `@engine_event(event_name, priority=0, namespace=None, system_name=None)`
声明网易原生事件 listener。handler 收到 `FrameworkEvent`，原始 args 位于 `event.data`。

### `FrameworkEvent`
字段：`name`、`data`、`source`、`target`、`context`、`result`。
方法：
- `cancel(engine_cancel_key=None)`：标记业务取消；传 key 时同步写入原生 args。
- `is_cancelled()`
- `stop_propagation()`
- `is_propagation_stopped()`

### `EventBus`
- `register(name, callback, priority=0, owner=None)`
- `register_owner(owner)`
- `unregister_owner(owner)`
- `emit(event_or_name, data=None, source=None, target=None, context=None)`
- `listeners(name=None)`

Listener 按 priority 从高到低执行。

## RPC

### `@rpc_server(endpoint)` / `@rpc_client(endpoint)`
声明 endpoint。handler 签名：`handler(ctx, data)`。

### `RPCContext`
字段：`side`、`endpoint`、`player_id`、`request_id`、`raw`、`runtime`。

服务端 `player_id` 来自引擎发送者标识；业务 data 不负责身份认证。

### `RPCManager`
客户端：
- `notify_server(endpoint, data)`
- `request_server(endpoint, data, callback)`
- 代理：`runtime.rpc.server.soldier.command(data)`

服务端：
- `notify_client(player_id, endpoint, data)`
- 代理：`runtime.rpc.client(player_id).ui.notice(data)`

`register_owner`/`unregister_owner` 由 FeatureManager 自动调用。

## Data

### Field
`StringField`、`IntField`、`FloatField`、`BoolField`、`ListField`、`DictField`。
公共参数：`default`、`nullable`、`validator`。

### Model
类属性：`storage_key`、`version`。方法：`fields()`、`to_dict()`、`from_dict()`。

### Repository
`Repository(model_class, backend, storage_key=None, cache=True, migrations=None)`。
- `load(subject_id, refresh=False)`
- `save(subject_id, model)`
- `delete(subject_id)`
- `invalidate(subject_id=None)`

### Backend
- `MemoryBackend`
- `ModAttrBackend(adapter, sync=True)`
- `ExtraDataBackend(adapter, sync=True)`
- `BlockEntityBackend(adapter)`；subject_id 为 `(dimension_id, pos)`。

### MigrationPlan
`add(from_version, callback)`；callback 接收旧 data dict，返回新 data dict。`migrate(data, from_version, to_version)` 顺序执行。

## Adapter

### `ServerAdapter`
公开薄封装：
`get_pos`、`get_foot_pos`、`set_pos`、`get_dimension`、`get_identifier`、`get_type_family`、`get_owner_id`、`get_attack_target`、`set_attack_target`、`reset_attack_target`、`trigger_entity_event`、`get_mod_attr`、`set_mod_attr`、`get_extra_data`、`set_extra_data`、`get_block_entity_data`、`get_surface_y`、`get_nearby_entities`、`create_entity`、`destroy_entity`、`add_timer`、`add_repeated_timer`。

### `ClientAdapter`
`local_player_id`、`get_pos`、`get_foot_pos`、`get_dimension`、`get_identifier`、`get_mod_attr`、`add_timer`。

Adapter 只减少重复组件创建；不要把它视为替代官方 ModAPI 文档的第二套引擎 API。

## Timer

### `TimerManager`
`once(delay, callback, *args)`、`repeat(interval, callback, *args)`、`inspect()`。

## UI

### `UIInfrastructureFeature`

Feature id：`ui`，client-only。注册 `ui` Registry 与 `ui` Service，并在 `UiInitFinished` 后调用 `ScreenManager.register_all()`。项目 UI Feature 应依赖 `ui` 并在 REGISTER 阶段注册 Screen。

### `UIRegistry`
`register_screen(screen_id, ui_name, python_path, screen_def, is_hud=False, source=None)`。

### `ScreenManager`
`register_all()`、`create(screen_id, options=None)`、`get(screen_id)`、`remove(screen_id)`。

### `PathResolver`
- `find_by_suffix(screen_node, root_path, suffix)`
- `find_all_by_suffix(...)`
- `child_by_name(control, name)`

这是为了避免 scrolling/grid 自动生成路径被硬编码。

### `UIController`
轻量 ScreenNode 组合基类，`find_path(root_path, suffix)`。

## Debug

### `Profiler`
`begin(category, name, callback=None)`、`end(token)`、`snapshot()`。默认关闭。

### `Inspector`
`features()`、`events(name=None)`、`rpc()`、`registries()`、`services()`、`timers()`、`profiler()`。

## Domain: Faction

Registry id：`faction`；Service id：`faction`。

`FactionRegistry.register_faction(faction_id, display_name=None, families=(), data=None, source=None)`。

`FactionService`：
- `get_player_faction(player_id)`
- `set_player_faction(player_id, faction_id) -> Result`
- `get_entity_faction(entity_id)`：优先读取显式 AWF entity faction ModAttr；若不存在，再读取已注册 SoldierType 默认阵营，最后按 type_family 匹配。
- `set_entity_faction(entity_id, faction_id)`

## Domain: Soldier

Registry id：`soldier_type`；Service id：`soldier`。

`register_soldier(soldier_id, entity_id, faction_id=None, tags=(), controllable=True, data=None, source=None)`。

`SoldierService`：`get_type(entity_id)`、`is_soldier(entity_id)`、`set_group(entity_id, group_id)`、`get_group(entity_id, default=0)`。

## Domain: Ownership

Service id：`ownership`。

`get_owner_id(entity_id)`、`is_owned_by(entity_id, player_id)`、`is_controllable_by(entity_id, player_id)`。

## Domain: Formation

Registry id：`formation`；Service id：`formation`。
内置：`line`、`column`、`grid`、`wedge`。

`FormationService.build_slots(center, count, formation_id="grid", dimension_id=0, spacing=1.5, forward=(0,1), adapt_surface=True) -> Result[list[pos]]`。

每个 slot 独立调用 `get_surface_y`；不会只给中心点算一次 Y。

## Domain: CombatRelation

Registry id：`combat_relation`；Service id：`combat_relation`。

Relation：`FRIENDLY`、`NEUTRAL`、`HOSTILE`。

`set_relation(first, second, relation, symmetric=True)`。

Service：`relation(first_faction, second_faction)`、`entity_relation(first_entity, second_entity)`、`can_damage(first_entity, second_entity, friendly_fire=False)`。

## Domain: Command

Registry id：`command`；Service id：`command`。支持运行时注册。

`register_command(command_id, handler, requires_target=False, radius=24, data=None, source=None)`。`radius` 由服务端注册定义，客户端不能覆盖。

handler 签名：`handler(ctx, entity_ids, target, params) -> Result | object`。

`CommandService.resolve_selection(player_id, selection, group_id=0, radius=24)`：
- `selection={"mode":"single","entity_id":...}`：重复做 owner/controllable 校验。
- `selection={"mode":"group"}`：服务端主动扫描玩家附近实体，按 owner + group 过滤。

`execute(ctx, command_id, selection=None, target=None, group_id=0, params=None)` 在 handler 前后发 `soldier.command.before_execute` / `soldier.command.after_execute`。

内置 server RPC endpoint：`soldier.command`。

## Domain: Resource

Registry id：`resource`；Service id：`resource`。

`register_resource(resource_id, display_name=None, minimum=0, data=None, source=None)`。

Service：`get_all`、`get`、`set`、`add`、`can_afford`、`consume`、`snapshot`、`restore`。

持久化模型：`PlayerResourceData.values`。

## Domain: Building

Registry id：`building`；Service id：`building`。

`register_building(building_id, costs=None, validator=None, placement_handler=None, data=None, source=None)`。

`build(player_id, building_id, context)`：validator -> 资源快照 -> 扣资源 -> placement -> 失败则资源回滚。

AWF 不猜结构放置 API；项目必须提供 `placement_handler`，这样 SDK 版本变化只影响 provider/Adapter 边界。

## Domain: Workbench

Registry id：`workbench`；Service id：`workbench`。

`register_workbench(workbench_id, recipes=None, data=None, source=None)`。

Recipe 推荐字段：`costs`、`max_count`、`output_handler`，其他字段可由项目自行附加供 UI 使用。

Service：`get_payload(player_id, workbench_id)`、`craft(player_id, workbench_id, recipe_id, count=1)`。

Workbench 永远通过 `workbench_id` 定位，不与某个测试物品绑定。

## Domain: Technology

Registry id：`technology`；Service id：`technology`。

`register_technology(tech_id, costs=None, prerequisites=(), faction_id=None, required_age=1, branch_group=None, target_age=None, data=None, source=None)`。

Service：`get_state(player_id)`、`has(player_id, tech_id)`、`research(player_id, tech_id)`。

持久字段：`researched`、`branches`、`age`。

## Domain: Spawn

Registry id：`spawn`；Service id：`spawn`。

`register_spawn(spawn_id, entity_id, events=(), data=None, source=None)`。

`spawn(spawn_id, pos, dimension_id=0, rot=(0,0))` 创建实体并按顺序触发配置的实体事件。

## Domain: Patrol

Registry id：`patrol`；Service id：`patrol`。

`register_patrol(patrol_id, members, weight=1, formation_id="grid", spacing=1.5, data=None, source=None)`，其中 `members={spawn_id: count}`。

Service：`choose(patrol_ids=None)`、`spawn_patrol(patrol_id, center, dimension_id=0, forward=(0,1))`。

生成结果返回全部成功生成的 runtime entity id。


# Runtime / Lifecycle / Logger

## `FrameworkRuntime`

公开字段：`side`、`system`、`config`、`lifecycle`、`logger`、`profiler`、`services`、`registries`、`event_bus`、`adapter`、`rpc`、`timers`、`engine_events`、`feature_manager`、`inspector`。

- `start()`：绑定 RPC，加载显式 Feature Manifest，依次 REGISTER / RESOLVE / FREEZE / RUNNING，并发送 `framework.started`。
- `shutdown()`：发送 `framework.before_shutdown`，逆序关闭 Feature，清空 Service。

## `Lifecycle`

常量：`BOOTSTRAP`、`REGISTER`、`RESOLVE`、`FREEZE`、`RUNNING`、`SHUTDOWN`。

## `Logger`

等级：`DEBUG`、`INFO`、`WARNING`、`ERROR`。公开方法：`debug(message)`、`info(message)`、`warning(message)`、`error(message)`。

# EngineEventRouter / RPC Proxy

## `EngineEventRouter`

`register_owner(owner)` 扫描 owner 上的 `@engine_event` metadata，并保证相同原生事件只向网易 System 注册一个 wrapper。原始事件之后进入 `EventBus`。

## `RPCNamespaceProxy`

由 `RPCManager.server` / `RPCManager.client(player_id)` 返回。属性链会拼成 endpoint，例如 `rpc.server.soldier.command(data)` -> `soldier.command`。它是调用便利层，真实网络边界仍由 `RPCManager` 处理。

# Data Backend 详细接口

所有 Backend 实现同一最小协议：

- `load(subject_id, storage_key)`
- `save(subject_id, storage_key, value)`
- `delete(subject_id, storage_key)`

`MemoryBackend` 用于内存数据；`ModAttrBackend` 用于玩家/实体 ModAttr；`ExtraDataBackend` 当前按 world/level ExtraData 使用，`subject_id` 不参与 key；`BlockEntityBackend` 的 `subject_id=(dimension_id, pos)`。

# Domain 类补充

每个 Domain Feature 的 Registry / Service / Feature 类名与完整方法签名均列在 `PUBLIC_API_INDEX.md`。其中：

- `FactionFeature` 注册 `FactionRegistry` / `FactionService` / `PlayerFactionData` Repository。实体阵营解析优先级为：显式 entity ModAttr -> 已注册 SoldierType 默认阵营 -> type_family 映射。
- `OwnershipService.is_controllable_by` 必须先满足 soldier.controllable、owner 一致；当玩家和实体双方都有阵营时，还必须阵营一致。
- `FormationProvider.offsets(count, spacing)` 是自定义阵型 provider 的扩展接口。内置实现为 `LineFormation`、`ColumnFormation`、`GridFormation`、`WedgeFormation`。
- `CommandFeature.rpc_command` 是内置 `soldier.command` endpoint。
- `ResourceService.consume` 拒绝未注册资源、非整数成本和负成本。

# 文档完整性

`API_REFERENCE.md` 描述公开 API 的行为契约；`PUBLIC_API_INDEX.md` 给出 v0.1.0 源码中所有公开符号和精确签名；`EVENT_RPC_REFERENCE.md` 列出内置事件/RPC；`ERROR_CODES.md` 列出业务 Result 失败码。四者共同构成 v0.1.0 的完整 API 文档集。

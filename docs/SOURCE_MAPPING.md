# AWF 设计来源与边界

本文档只记录适合公开仓库的设计来源、通用工程经验与边界，不包含任何具体商业/私有游戏项目的目录、代号、内部模块清单、开发路线或未公开资产信息。

## QuModLibs -> AWF Core

AWF v0.1.0 对 QuModLibs v1.4 中若干成熟框架机制进行了选择性重写与重新组织。

| QuModLibs 中的思路 | AWF 落地 | AWF 的差异 |
|---|---|---|
| Feature 作为业务边界 | `Core/Feature` | 使用显式 Manifest 与 dependency graph，不使用 import 即注册 |
| `@Listen` | `@event` / `@engine_event` | 装饰器只保存 metadata；注册发生在 Feature 生命周期 |
| 单 Loader/System 聚合 | `AWFServerSystem` / `AWFClientSystem` + `FrameworkRuntime` | Service、Registry 与生命周期全部显式化 |
| `@AllowCall` / `Call` | `@rpc_server` / `@rpc_client` / RPC proxy | endpoint 使用稳定名称，并支持 `Result` 序列化 |
| `@InjectRPCPlayerId` | `RPCContext.player_id` | 调用身份进入框架 Context，不依赖业务 payload 中的玩家 ID |
| Destroy 生命周期 | `Feature.disable()` + Runtime shutdown | 按依赖逆序关闭 |

具体署名与许可证见 `THIRD_PARTY_NOTICES.md` 和 `licenses/QuModLibs-BSD-3-Clause.txt`。

## 通用古代战争项目经验 -> AWF Domain

AWF Domain 来自对古代战争类 MODSDK 项目中反复出现的问题进行抽象，而不是复制某一个完整游戏项目。

| 通用工程问题 | AWF 落地 |
|---|---|
| 事件监听散落、生命周期不明确 | Event metadata + EventBus + EngineEventRouter + Feature lifecycle |
| 单个 System 承担过多不相关业务 | 显式 Feature + Service / Registry 分离 |
| 工作台触发方式与配方数据强耦合 | `WorkbenchRegistry` / `WorkbenchService`，通过稳定 `workbench_id` 寻址 |
| 内容数据缺少统一注册边界 | `Registry` / `RegistryHub` |
| 指挥系统需要 ownership / faction / group 等多层服务端过滤 | `OwnershipService` + `FactionService` + `CommandService` |
| “谁接受命令”和“命令作用目标”被混为一个 pointer | Command 的 `selection` / `target` / `command` 三层语义 |
| 高频全世界扫描导致性能问题 | 按命令定义 radius，在执行时按需扫描候选实体 |
| 阵列跨越起伏地形时出现埋地/悬空 | `FormationService.build_slots()` 对每个 slot 独立解析 surface Y |
| 友伤规则散落在伤害回调中 | `CombatRelationService` 提供独立关系判断 |
| 玩家资源、科技等状态被客户端或临时 UI 值驱动 | Repository + server-authoritative Domain Service |
| 扣除资源后外部操作失败造成不一致 | Resource snapshot + rollback 事务边界 |
| MODSDK UI 自动生成节点路径不稳定 | `PathResolver.find_by_suffix()` / `child_by_name()` |
| 不同 AddOn 之间直接 import 工具代码形成隐藏依赖 | AWF 源码随使用它的 AddOn 内置 |

这些规则是领域层的工程抽象，并不包含任何具体作品的兵种表、阵营表、建筑资产、配方、科技树、AI、数值或世界生成内容。

## v0.1.0 暂未固化的领域

以下能力当前不属于 v0.1.0 的标准 Domain Manifest：

- Shield
- Warehouse
- Raid
- Occupation
- WorldEvent
- Dialogue
- FactionEffect

这只代表当前框架范围，不代表任何外部项目是否实现了这些功能。现有 Feature / Event / Registry / Model / Service 机制可以作为未来扩展基础。

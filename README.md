# Ancient War Framework v0.1.0

适用于网易《我的世界》MC_MOD / MODSDK 开发的古代战争类玩法框架。

> 本项目基于 [QuModLibs](https://github.com/GitHub-Zero123/QuModLibs) 修改与扩展而来，在其事件注册、RPC 通信与单入口加载等设计基础上，重新组织了 Feature 生命周期、Service、Registry、Data 与古代战争 Domain 层。
>
> QuModLibs 原项目采用 BSD 3-Clause License，相关署名与许可证文本已保留在 `THIRD_PARTY_NOTICES.md` 与 `licenses/QuModLibs-BSD-3-Clause.txt` 中。

## 版本说明

当前版本为 `v0.1.0`，主要完成 AWF Core 与第一批古代战争 Domain 的框架化实现。

AWF 当前定位为**开发框架 / 工具层**，不是可以直接游玩的完整古代战争模组。仓库不包含完整兵种实体、模型贴图、建筑结构、AI、战役内容、固定阵营、科技树与数值平衡等具体作品资产。

目前主要包含：

- Feature 与生命周期管理；
- Event Bus 与原生 MODSDK Event 路由；
- Client / Server RPC；
- Service Container；
- Registry 与内容注册；
- Model / Repository / Backend / Migration；
- Timer、UI 与 Debug 基础设施；
- Faction、Soldier、Ownership、Command、Formation、Resource 等古代战争领域抽象。

> `v0.1.0` 已完成源码与静态一致性检查，但仍属于早期版本，具体 MODSDK 行为应在目标网易版本与 MC Studio 环境中实际验证。

## 创建项目

您可以通过以下方式将 `AncientWarFramework` 内置到自己的网易 MCMOD 项目中。

### 项目结构

推荐将 AWF 直接放入当前 AddOn 的行为包脚本目录中：

```text
├── behavior_pack_xxx
│   ├── YourGameScripts
│   │   ├── __init__.py
│   │   ├── modMain.py
│   │   └── modConfig.py
│   │
│   └── AncientWarFramework
│       ├── Bootstrap
│       ├── Core
│       ├── Domain
│       ├── __init__.py
│       └── version.py
```

AWF 推荐采用**源码内嵌分发**。每个 AddOn 携带自己使用的框架副本，不依赖另一个已经加载的 AddOn 提供 Python import 路径。

### 配置系统

```python
# modConfig.py
# -*- coding: utf-8 -*-

ModName = "YourAncientWarGame"
ModVersion = "0.0.1"

ServerName = "YourGameServer"
ClientName = "YourGameClient"

ServerPath = "AncientWarFramework.Bootstrap.ServerSystem.AWFServerSystem"
ClientPath = "AncientWarFramework.Bootstrap.ClientSystem.AWFClientSystem"
```

在 `RegisterSystem` 之前配置 AWF：

```python
# modMain.py
# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

import modConfig

from AncientWarFramework import FrameworkConfig, configure
from AncientWarFramework.Domain import STANDARD_DOMAIN_FEATURES


configure(FrameworkConfig(
    mod_name=modConfig.ModName,
    server_name=modConfig.ServerName,
    client_name=modConfig.ClientName,
    features=STANDARD_DOMAIN_FEATURES,
    dev_mode=True,
    profiler_enabled=False,
))


@Mod.Binding(name=modConfig.ModName, version=modConfig.ModVersion)
class YourGameMod(object):

    @Mod.InitServer()
    def server_init(self):
        serverApi.RegisterSystem(
            modConfig.ModName,
            modConfig.ServerName,
            modConfig.ServerPath,
        )

    @Mod.InitClient()
    def client_init(self):
        clientApi.RegisterSystem(
            modConfig.ModName,
            modConfig.ClientName,
            modConfig.ClientPath,
        )
```

如果项目不需要全部 Domain，请自行维护 `FEATURES = (...)`，只加载实际使用的 Feature。

### 开发范式建议

AWF 以 **Feature（业务特性）** 作为主要功能边界，但与 QuModLibs 的 `import` 即初始化方式不同：AWF 的装饰器主要保存 metadata，真正的注册、依赖解析、启用与关闭由 Framework Runtime 显式管理。

一个 Feature 可以声明：

- `feature_id`：稳定的功能 ID；
- `dependencies`：依赖的其他 Feature；
- `sides`：运行于 Server、Client 或双端；
- `register()`：注册内容、事件、Service 等；
- `resolve()`：解析依赖；
- `enable()`：启用功能；
- `disable()`：关闭与清理。

推荐将项目自身内容通过独立 Feature 注册到 AWF，而不是直接修改框架源码。

```python
class YourServerFeature(Feature):
    feature_id = "your_server"
    sides = ("server",)
    dependencies = ("faction", "resource")


class YourClientFeature(Feature):
    feature_id = "your_client"
    sides = ("client",)
    dependencies = ("ui",)
```

## 事件监听

AWF 提供框架事件和原生 MODSDK Event 两种入口。

### 框架事件

```python
from AncientWarFramework.Core.Event.Decorators import event


@event("resource.changed")
def on_resource_changed(self, event):
    player_id = event.data.get("player_id")
    resource_id = event.data.get("resource_id")
```

### MODSDK 原生事件

```python
from AncientWarFramework.Core.Event.Decorators import engine_event


@engine_event("ServerPlayerTryDestroyBlockEvent")
def on_destroy_block(self, event):
    args = event.data
    player_id = args.get("playerId")
```

`@engine_event` 默认使用当前端的 Engine Namespace / System Name，并由 `EngineEventRouter` 统一完成监听与分发。

AWF 的 Event 支持：

- priority；
- `event.cancel()`；
- `event.stop_propagation()`；
- Feature owner 生命周期清理；
- 原生事件与框架事件统一调度。

## RPC 通信

AWF 的 RPC 设计参考了 QuModLibs 的 `@AllowCall` / `Call` / `@InjectRPCPlayerId`，但重新设计为 endpoint + `RPCContext` 的形式。

### 声明服务端 RPC

```python
from AncientWarFramework.Core.RPC.Decorators import rpc_server
from AncientWarFramework import Result


@rpc_server("your.endpoint")
def on_request(self, ctx, data):
    # ctx.player_id 来自 RPC 接收事件上下文
    player_id = ctx.player_id
    return Result.success()
```

服务端不应直接相信客户端 payload 中传入的 `player_id`，需要玩家身份时应使用 `RPCContext.player_id`。

### Client -> Server

```python
self.runtime.rpc.server.your.endpoint(data)
```

需要回调时：

```python
self.runtime.rpc.request_server("your.endpoint", data, callback)
```

### Server -> Client

```python
self.runtime.rpc.client(player_id).your.endpoint(data)
```

AWF 使用稳定 endpoint 名称进行通信，避免业务层直接维护大量底层自定义事件细节。

## Registry 与 Service

AWF 将“内容定义”和“运行行为”分开处理。

### Registry

Registry 适合保存：

- 阵营定义；
- 兵种定义；
- 指令定义；
- 阵型定义；
- 资源类型；
- 建筑；
- 工作台与配方；
- 科技；
- Spawn / Patrol 配置。

例如项目可以在自己的 Feature 中注册阵营：

```python
registry = self.runtime.registries.require("faction")
registry.register_faction(
    "kingdom",
    "Kingdom",
    families=("kingdom",),
)
```

Registry 支持生命周期约束与 Freeze，减少运行期被任意代码修改配置的风险。

### Service

Service 用于提供行为能力，例如：

- `FactionService`：解析玩家 / 实体阵营；
- `OwnershipService`：判断实体归属与控制权限；
- `CommandService`：筛选单位并执行指令；
- `FormationService`：计算阵列 slot；
- `CombatRelationService`：判断阵营关系与伤害许可；
- `ResourceService`：服务端资源读写与事务；
- `WorkbenchService`：工作台合成事务；
- `TechnologyService`：科技升级；
- `PatrolService`：巡逻队生成。

## 古代战争 Domain

`v0.1.0` 默认提供以下 Domain Feature：

| Domain           | 用途                     |
| ---------------- | ------------------------ |
| `Faction`        | 阵营定义与阵营解析       |
| `Soldier`        | 士兵类型与元数据         |
| `Ownership`      | 所有者关系与可控制性     |
| `Command`        | 士兵指挥与服务端过滤     |
| `Formation`      | 阵型 slot 与地形适配     |
| `CombatRelation` | 阵营关系与伤害许可       |
| `Resource`       | 服务端资源与事务         |
| `Building`       | 建筑定义、成本与放置接口 |
| `Workbench`      | 工作台与配方事务         |
| `Technology`     | 科技定义与研究           |
| `Spawn`          | 通用实体生成定义         |
| `Patrol`         | 巡逻队组成与批量生成     |

可以直接使用：

```python
from AncientWarFramework.Domain import STANDARD_DOMAIN_FEATURES
```

### Command 指挥模型

AWF 将指挥系统中的三个概念明确分开：

```python
selection = {
    "mode": "single",
    "entity_id": "...",
}  # 谁接受命令

target = {
    "type": "entity",
    "entity_id": "...",
}  # 命令作用到哪里 / 谁

command_id = "march"  # 做什么
```

避免使用同一个 pointer 同时表示“被指挥单位”和“攻击目标”。

### Formation 阵型

Formation 只负责计算位置，不直接实现实体 AI。

推荐流程：

```text
Command
  -> 获取 entity_ids
  -> FormationService 生成 slots
  -> 每个士兵取得独立 slot
  -> 项目自己的 MoveTo / CustomGoal 执行移动
```

跨越起伏地形时，每个 slot 会独立解析 surface Y，避免所有单位共用同一个高度。

## Data 数据层

AWF 提供：

- `Field`；
- `Model`；
- `Repository`；
- `MemoryBackend`；
- `ModAttrBackend`；
- `ExtraDataBackend`；
- `BlockEntityBackend`；
- `MigrationPlan`。

用于将“数据结构”“缓存”“持久化方式”与具体业务 Service 分离。

长期玩家状态不建议直接保存在全局 Service 实例字段中，而应使用 Repository / Backend 按主体 ID 管理。

## UI

AWF Core 提供基础 UI Infrastructure：

- `UIRegistry`；
- `ScreenManager`；
- `Controller`；
- `PathResolver`；
- `UIInfrastructureFeature`。

其中 `PathResolver` 可用于处理网易 UI 中动态生成的节点路径，减少对完整控件路径的硬编码。

AWF 只提供 UI 工程基础设施，不提供固定的古代战争视觉界面或美术资源。

## Debug

开发模式下可以使用 AWF Debug 模块查看 Runtime 状态，包括：

- Feature；
- Event；
- RPC endpoint；
- Registry；
- Service；
- Timer；
- Profiler。

Profiler 默认可以关闭，避免正式环境产生不必要的调试开销。

## 与 QuModLibs 的关系

Ancient War Framework **不是从零开始独立设计的框架**。

本项目基于 [QuModLibs](https://github.com/GitHub-Zero123/QuModLibs) 修改与扩展，选择性参考并重写了 QuModLibs v1.4 中的部分框架机制，主要包括：

- 装饰器形式的 Event 注册思路；
- RPC 函数注册与跨端调用思路；
- RPC 调用来源玩家注入 / 识别思路；
- 单 Loader / Root System 聚合生命周期的思路。

AWF 在此基础上进一步增加或重新设计了：

- 显式 Feature Manifest 与依赖解析；
- 显式生命周期，而非依赖 `import` 副作用完成全部初始化；
- Service Container；
- Registry / RegistryHub；
- Data Model / Repository / Backend；
- `RPCContext`；
- EventBus / EngineEventRouter；
- 古代战争 Domain 层；
- Resource Transaction；
- Formation、Command、Faction、Ownership 等领域服务。

涉及 QuModLibs 的派生设计在相关源码注释中进行了标注。

QuModLibs 原作者及项目版权归原作者所有，原项目地址：

[https://github.com/GitHub-Zero123/QuModLibs](https://github.com/GitHub-Zero123/QuModLibs)

QuModLibs 使用 BSD 3-Clause License，许可证副本见：

```text
licenses/QuModLibs-BSD-3-Clause.txt
```

更完整的第三方说明见：

```text
THIRD_PARTY_NOTICES.md
```

## 文档

仓库中提供了进一步的框架说明：

| 文档                          | 内容               |
| ----------------------------- | ------------------ |
| `docs/INTEGRATION.md`         | 新项目接入 AWF     |
| `docs/ARCHITECTURE.md`        | Runtime 与整体架构 |
| `docs/API_REFERENCE.md`       | API 参考           |
| `docs/PUBLIC_API_INDEX.md`    | 公开符号索引       |
| `docs/EVENT_RPC_REFERENCE.md` | Event / RPC 说明   |
| `docs/DOMAIN_GUIDE.md`        | Domain 使用约束    |
| `docs/DESIGN_DECISIONS.md`    | 设计决策           |
| `docs/DEBUGGING.md`           | 调试方式           |
| `docs/ERROR_CODES.md`         | 错误码说明         |
| `docs/SOURCE_MAPPING.md`      | 公开设计来源与边界 |

## 当前不包含的功能

以下内容目前没有作为 `v0.1.0` 标准 Domain 固化：

- Shield；
- Warehouse；
- Raid；
- Occupation；
- WorldEvent；
- Dialogue；
- FactionEffect。

它们可以在后续版本中基于现有 Feature / Event / Registry / Service 机制继续扩展。

## Python / MODSDK 兼容

AWF 面向网易 MODSDK 常见的 Python 2.7 风格环境开发。

请避免在框架或业务代码中直接使用：

- f-string；
- Python 3 类型注解；
- dataclass；
- match / case；
- pathlib 等 Python 3-only API。

具体 MODSDK Event、Component、字段和方法签名仍应以目标网易版本的官方文档与实际 MC Studio 环境为准。

## License

QuModLibs 派生部分保留 BSD 3-Clause License 的版权与许可证声明。

当前 `v0.1.0` 仓库尚未为 **Ancient War Framework 自身新增代码**指定独立的仓库级 LICENSE。在正式以开源项目形式发布前，建议明确选择 AWF 自身的许可证，并继续保留 QuModLibs 的 BSD 3-Clause 版权声明与第三方通知。

## 更多功能

更多实现细节请查看 `docs/`、`AncientWarFramework/Core/`、`AncientWarFramework/Domain/` 中的文档和源码注释。
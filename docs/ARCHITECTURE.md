# AWF 架构

## 1. 分层

```text
Project modMain.py
    -> AWFServerSystem / AWFClientSystem
        -> FrameworkRuntime
            -> FeatureManager
            -> EventBus / EngineEventRouter
            -> RPCManager
            -> ServiceContainer
            -> RegistryHub
            -> Data Repository
            -> Timer / UI / Debug
                -> Domain Features
```

Core 不理解“阵营/士兵/科技”的业务含义；Domain 基于 Core 实现古代战争通用语义。

## 2. 生命周期

`BOOTSTRAP -> REGISTER -> RESOLVE -> FREEZE -> RUNNING -> SHUTDOWN`

- REGISTER：Feature 注册 Registry 与 Service。
- RESOLVE：Feature 获取依赖并完成交叉绑定。
- FREEZE：默认 Registry 进入只读。
- RUNNING：接收 Engine Event / RPC。
- SHUTDOWN：逆依赖顺序 disable。

## 3. Feature 依赖

Feature 必须有稳定 `feature_id` 与显式 `dependencies`。`FeatureManager` 在启动阶段做拓扑排序；缺依赖或循环依赖直接抛 `FeatureDependencyError`。

## 4. 事件

`@event` 与 `@engine_event` 只在方法上保存 metadata。实际注册发生在 Feature REGISTER 阶段，因此 import 模块不会偷偷修改全局状态。

Domain Event 支持 priority、cancel、stop propagation、result/context。

## 5. RPC

客户端通过一个 C2S 自定义事件发送 endpoint；服务端通过 S2C 事件返回/推送。服务端 handler 的玩家身份来自引擎事件中的发送者标识，不从业务 payload 读取。

## 6. 数据

一个 Model 默认持久化为：

```python
{"version": 1, "data": {...}}
```

Repository 负责默认值、缓存、保存和 migration；Backend 决定最终落到 ModAttr / ExtraData / BlockEntityData。

## 7. Domain 语义边界

- Faction：阵营定义与实体/玩家阵营解析。
- Soldier：兵种定义、兵种识别、编组字段。
- Ownership：owner 与可控性。
- Command：selection / target / command 分离。
- Formation：只计算 slot；每个 slot 独立取 surface Y。
- CombatRelation：阵营关系与是否允许伤害。
- Resource：玩家资源事务。
- Building：成本 + validator + placement provider。
- Workbench：workbench_id -> recipes，与触发物品解耦。
- Technology：前置/时代/分支/成本。
- Spawn：单实体生成定义。
- Patrol：实体组成 + 阵型 + 批量生成。

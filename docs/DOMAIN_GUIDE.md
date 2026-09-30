# Domain 使用约束

## Command 的三种语义必须分开

```python
selection = {"mode": "single", "entity_id": "..."}  # 谁接受命令
# 或 {"mode": "group"}

target = {"type": "entity", "entity_id": "..."}     # 命令作用到哪里/谁
command_id = "march"                                   # 做什么
```

不要重新让一个 `pointerData` 同时表示“被指挥士兵”和“攻击目标”。

## Formation

Formation 只负责 slot，不负责 AI。推荐流程：

1. Command handler 获取 entity_ids。
2. FormationService 生成相同数量的 slots。
3. 每个士兵只消费自己的 slot。
4. MoveTo/CustomGoal 由作品自己的 Soldier 行为代码实现。

## CombatRelation

`can_damage()` 只回答关系规则，不负责自动清仇恨。若作品实现友伤关闭，应在“拒绝伤害”的同时通过 Combat Feature / Domain Event 清理非法友军 attack target。

## Resource Transaction

Building、Workbench、Technology 都依赖 ResourceService。任何会产生外部副作用的操作都应先保存 snapshot，并在失败时 restore。

## Building

AWF 不内置特定 `.mcstructure` 放置实现；网易结构 API、BuildingSystem 或大型特征的接口随作品和 SDK 变化较大。通过 `placement_handler` 注入项目当前已验证的实现。

## Registry 数据

v0.1.0 采用 Python 配置。推荐作品建立单独 `db/` 或 `config/` 模块，然后由一个项目 Feature 在 REGISTER 阶段批量注册。

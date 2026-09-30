# Event / RPC Reference

## AWF 生命周期事件

| 事件 | 端 | data | 说明 |
|---|---|---|---|
| `framework.started` | 双端 | `side` | 当前 Runtime 完成 Feature enable 后触发 |
| `framework.before_shutdown` | 双端 | `side` | Feature 逆序 disable 前触发 |
| `registry.before_change` | 双端 | `registry`, `action`, `key`, 可选 `value` | 仅支持运行期修改的 Registry；可 `event.cancel()` 阻止变更 |
| `registry.changed` | 双端 | 同上 | 运行期 Registry 变更成功后触发 |

## Domain 事件

| 事件 | data | 时机 |
|---|---|---|
| `faction.player_changed` | `player_id`, `faction_id` | 玩家阵营写入成功 |
| `soldier.command.before_execute` | `ctx`, `command_id`, `entities`, `target`, `params` | Command handler 前；可取消 |
| `soldier.command.after_execute` | `ctx`, `command_id`, `entities`, `target`, `result` | Command handler 后 |
| `resource.changed` | `player_id`, `resource_id`, `value` | 单项资源 `set/add` 成功 |
| `building.placed` | `player_id`, `building_id`, `context` | placement 成功且资源事务提交 |
| `workbench.crafted` | `player_id`, `workbench_id`, `recipe_id`, `count` | output handler 成功 |
| `technology.researched` | `player_id`, `tech_id` | 科技研究成功 |
| `spawn.entity_created` | `spawn_id`, `entity_id` | 单实体生成成功 |
| `patrol.spawned` | `patrol_id`, `entity_ids` | 巡逻队生成流程完成 |

## Engine Event 路由

`@engine_event("EventName")` 默认使用当前端 `GetEngineNamespace()` / `GetEngineSystemName()`。内部总线名为：

```text
engine:<namespace>:<system_name>:<event_name>
```

handler 接收 `FrameworkEvent`，网易原始 `args` 保存在 `event.data`。`event.cancel(engine_cancel_key)` 可以同时将指定原始 args 字段写为 `True`；不同事件使用哪个取消字段仍以当前官方 ModAPI 文档为准。

## 内置 RPC endpoint

### `soldier.command`（Client -> Server）

请求 data：

```python
{
    "command_id": "march",
    "selection": {"mode": "group"},
    "group_id": 0,
    "target": None,
    "params": {},
}
```

服务端不会从 data 读取身份；`RPCContext.player_id` 来自 RPC 接收事件的引擎发送者标识。命令搜索半径来自服务端 `CommandRegistry` 定义，客户端不能覆盖。

## 自定义 RPC

服务端 endpoint：

```python
@rpc_server("your.endpoint")
def on_request(self, ctx, data):
    # type: (RPCContext, dict) -> Result
    return Result.success()
```

客户端调用：

```python
self.runtime.rpc.server.your.endpoint(data)
```

如需要响应回调，直接调用：

```python
self.runtime.rpc.request_server("your.endpoint", data, callback)
```

服务端推送客户端：

```python
self.runtime.rpc.client(player_id).your.endpoint(data)
```

# Error / Result Code Reference

正常业务拒绝使用 `Result.fail(code, data=None, message=None)`。下表来自 v0.1.0 源码中的公开失败码。

| code | 含义 |
|---|---|
| `age_locked` | 时代条件不满足 |
| `already_researched` | 已研究 |
| `branch_locked` | 互斥分支已选择其他科技 |
| `command_cancelled` | before_execute 事件取消 |
| `invalid_count` | 合成数量非法 |
| `invalid_group_id` | group_id 无法转换为有效组号 |
| `invalid_position` | 建筑 validator 拒绝 |
| `invalid_resource_cost` | 成本不是非负整数 |
| `invalid_selection_mode` | selection.mode 非 single/group |
| `missing_prerequisite` | 缺少前置科技 |
| `no_responsive_soldiers` | 选择结果为空 |
| `not_controllable` | 目标士兵不属于/不可由请求玩家控制 |
| `not_enough_resource` | 资源不足 |
| `output_failed` | 产出 handler 返回 False |
| `placement_failed` | placement provider 返回 False |
| `placement_handler_missing` | 建筑没有 placement provider |
| `resource_below_minimum` | 写入值低于资源 minimum |
| `rpc_endpoint_not_found` | 服务端 RPC endpoint 不存在 |
| `rpc_internal_error` | 服务端 endpoint 抛出异常且转换为安全失败结果 |
| `spawn_failed` | 实体创建失败 |
| `target_required` | 命令要求 target 但未提供 |
| `unknown_building` | 建筑未注册 |
| `unknown_command` | 命令未注册 |
| `unknown_faction` | 阵营未注册 |
| `unknown_formation` | 阵型未注册 |
| `unknown_patrol` | 巡逻队未注册 |
| `unknown_recipe` | 配方未注册 |
| `unknown_resource` | 资源未注册 |
| `unknown_spawn` | 生成定义未注册 |
| `unknown_technology` | 科技未注册 |
| `unknown_workbench` | 工作台未注册 |
| `wrong_faction` | 阵营条件不满足 |

框架结构错误不会转成上述业务码，而是使用 `AWFError` 子类异常。RPC endpoint 内未捕获异常默认对客户端返回 `rpc_internal_error`；开发模式可通过 `raise_rpc_errors=True` 让异常继续抛出。

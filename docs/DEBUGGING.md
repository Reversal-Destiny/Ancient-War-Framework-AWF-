# Debug / Profiler

`runtime.inspector` 可查看当前框架结构：

```python
runtime.inspector.features()
runtime.inspector.events()
runtime.inspector.rpc()
runtime.inspector.registries()
runtime.inspector.services()
runtime.inspector.timers()
runtime.inspector.profiler()
```

Profiler 通过 `FrameworkConfig(profiler_enabled=True)` 开启。正式发行建议关闭。

推荐出现“军令无响应”时依次检查：

1. `ownership.is_controllable_by`；
2. Soldier Registry 是否识别 entity identifier；
3. group ModAttr；
4. Command selection mode；
5. 扫描 radius；
6. handler 是否注册到 CommandRegistry；
7. RPC `soldier.command` 是否收到真实 sender identity。

出现 Feature 启动失败时先读异常；缺依赖、循环依赖、重复 Registry key 都应在 RUNNING 前失败，而不是静默跳过。

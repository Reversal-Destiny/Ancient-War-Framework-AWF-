# AWF v0.1.0 设计决策

本文记录首版冻结的架构决策，避免后续作品在基础层反复摇摆。

1. **QuModLibs 关系**：选择性移植/重写 Event、RPC、Loader/Lifecycle 思路；衍生设计直接融合进 Core，并保留第三方声明。
2. **分发方式**：源码内置。每个作品携带自己的 `AncientWarFramework/`，禁止依赖另一个 AddOn 的 Python 目录。
3. **分层**：Core 技术层 + Ancient War Domain 领域层。
4. **领域扩展**：组合 + Registry，不建立深继承树。
5. **风格**：统一 AWF 风格；Python 2.7 兼容，类 PascalCase，方法/变量 snake_case，`entity_id` / `player_id`。
6. **旧项目兼容**：v0.1.0 不承诺兼容任何既有项目的私有 API；历史项目只作为通用工程经验与失败模式来源。
7. **网易 System**：一个 `AWFServerSystem` + 一个 `AWFClientSystem`。
8. **Event**：完整 Event 对象，支持 priority / cancel / stop propagation / result / context。
9. **RPC**：显式 endpoint + 调用代理；服务端身份来自引擎发送者上下文。
10. **数据**：轻量 Model / Field / Repository / Backend / Migration。
11. **ModAPI**：只做薄 Adapter，不建立第二套 Entity API。
12. **Feature**：显式 Manifest + 依赖图 + 拓扑排序；同级节点保持 Manifest 声明顺序。
13. **Service**：单例/无 per-player 状态；状态进入 Model/Repository，调用身份进入 Context。
14. **Registry**：BOOTSTRAP → REGISTER → RESOLVE → FREEZE → RUNNING；默认冻结，特定 Registry 可允许运行期修改。
15. **v1 Domain**：Faction、Soldier、Ownership、Command、Formation、CombatRelation、Resource、Building、Workbench、Technology、Spawn、Patrol。
16. **UI**：只提供 UI 工程基础设施，不提供统一视觉组件库。
17. **诊断**：Logger + Inspector + 可关闭 Profiler。
18. **内容配置**：Python 为主；只有网易资源格式继续使用 JSON。
19. **装饰器**：Event/RPC 装饰器只记录 metadata；Feature/Service/Registry 显式注册。
20. **第三方代码位置**：直接融合到 Core，不单独维护运行时 ThirdParty 包。
21. **Demo**：v1 不提供 Demo/Starter。
22. **测试**：v1 暂不建设自动化测试/网易 Mock；问题以 MC Studio 实际反馈继续修。
23. **错误处理**：框架结构错误抛异常；正常业务拒绝返回 `Result`。
24. **SDK 兼容**：当前开发环境优先；未来版本差异收敛到 Adapter/Bootstrap。
25. **正式名称**：Ancient War Framework，简称 AWF；根包 `AncientWarFramework`，短命名空间 `awf`。

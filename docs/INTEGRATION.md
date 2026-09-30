# 集成到新作品

AWF 不提供 Demo，也不硬编码作品自己的 ModName。项目必须在 RegisterSystem 前配置 AWF。

## 1. 推荐路径

```text
behavior_pack_xxx/
  YourGameScripts/
    modMain.py
    modConfig.py
  AncientWarFramework/
    ...
```

## 2. modConfig.py

```python
# -*- coding: utf-8 -*-
ModName = "YourAncientWarGame"
ModVersion = "0.0.1"
ServerName = "YourGameServer"
ClientName = "YourGameClient"
ServerPath = "AncientWarFramework.Bootstrap.ServerSystem.AWFServerSystem"
ClientPath = "AncientWarFramework.Bootstrap.ClientSystem.AWFClientSystem"
```

## 3. modMain.py

```python
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
        serverApi.RegisterSystem(modConfig.ModName, modConfig.ServerName, modConfig.ServerPath)

    @Mod.InitClient()
    def client_init(self):
        clientApi.RegisterSystem(modConfig.ModName, modConfig.ClientName, modConfig.ClientPath)
```

如果作品不需要全部 Domain Feature，请自己显式维护 `FEATURES = (...)`，不要为了方便加载未使用系统。

## 4. 注册项目内容

建议建立项目自己的初始化 Feature，并依赖 AWF Domain Feature，在 `register()` 中填充 Registry。例如阵营配置应通过：

```python
registry = self.runtime.registries.require("faction")
registry.register_faction("kingdom", "Kingdom", families=("kingdom",))
```

这比直接修改 AWF 源码更适合后续多作品复用。

## 5. 自定义 Feature 的端侧约束

`FeatureManager` 会先按当前端过滤 `sides`，再校验依赖。因此不要让一个双端 Feature 依赖 server-only Feature。需要同时存在客户端与服务端业务时，建议拆成两个 Feature：

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

两端通过 AWF RPC endpoint 交互，不共享运行期 Python 对象。
